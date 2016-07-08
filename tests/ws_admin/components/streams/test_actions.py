import asyncio
from unittest import TestCase
from unittest.mock import MagicMock
from sqlalchemy.testing.assertions import AssertsCompiledSQL

from ws_admin.components.streams import actions
from ws_admin.components.streams import exc

from ikcms.orm import Mapper
from ikcms.utils.asynctests import asynctest

from ws_admin.components.streams.stream import Stream
from ws_admin.components.streams.forms import list_fields
from ws_admin.components.streams.forms import filter_fields
from ws_admin.components.streams.forms import item_fields
from tests.models import models1


TEST_DB_ID = 'test_db_id'


def with_transaction(test):
    def wrapper1(coroutine):
        def wrapper2(conn, *args, **kwargs):
            test.assertIsInstance(conn, test.env.app.db.ConnMock)
            test.assertEqual(conn.tn.state, 'begin')
            return coroutine(conn, *args, **kwargs)
        return wrapper2
    return wrapper1


def not_call(*args, **kwargs):
    raise AssertionError


class ActionsTestCase(TestCase, AssertsCompiledSQL):

    __dialect__ = 'default'

    def setUp(self):

        class FormFieldMock:
            enable_order = False
            enable_filter = False
            _widget = None

            def __init__(self, **kwargs):
                self.__dict__.update(kwargs)

            def __call__(self, context=None, parent=None):
                self.context = context
                return self

            def to_python(self, values):
                value = values.get(self.name)
                if value is not None:
                    if value==exc.ValidationError:
                        raise value({self.name: 'error'})
                    return {self.name: '{}-to_python'.format(value)}
                else:
                    return {}

            def from_python(self, value):
                return {self.name: '{}-from_python'.format(value.get(self.name))}

            def get_initials(_self, test_kwarg='test_default'):
                self.assertIn(test_kwarg, ['test_default', 'test_init'])
                return '{}-{}-initials'.format(_self.name, test_kwarg)

            order = list_fields.simple_order
            filter = filter_fields.eq_filter

            @property
            def widget(self):
                return MagicMock(to_dict=MagicMock(return_value=self._widget))


        class TestStream(Stream):
            max_limit = 50
            name = 'test_stream'
            title = 'test_stream_title'
            mapper = Mapper(models1.test_table1, {}, TEST_DB_ID)

            list_fields = [
                    FormFieldMock(
                        name='id',
                        enable_order=True,
                        _widget='ID_LIST_WIDGET',
                    ),
                    FormFieldMock(
                        name='title',
                        enable_order=True,
                        _widget='TITLE_LIST_WIDGET',
                    ),
            ]
            filter_fields = [
                    FormFieldMock(
                        name='id',
                        enable_filter=True,
                        _widget='ID_FILTER_WIDGET',
                    ),
                    FormFieldMock(
                        name='title',
                        enable_filter=True,
                        _widget='TITLE_FILTER_WIDGET',
                    ),
                    FormFieldMock(
                        name='title2',
                        enable_filter=True,
                        _widget='TITLE2_FILTER_WIDGET',
                    ),
            ]
            item_fields = [
                    FormFieldMock(name='id', _widget='ID_ITEM_WIDGET'),
                    FormFieldMock(name='title', _widget='TITLE_ITEM_WIDGET'),
            ]


        class TnMock:
            state = 'new'
            async def __aenter__(self):
                assert self.state == 'new'
                self.state = 'begin'

            async def __aexit__(self, *args):
                assert self.state == 'begin'
                self.state = 'close'


        class DBMock:
            tns = []

            class ConnMock:
                def __init__(self, db):
                    self.db = db
                    self.tn = None

                async def begin(self):
                    self.tn = TnMock()
                    self.db.tns.append(self.tn)
                    return self.tn

                async def __aenter__(self, *args):
                    return self

                async def __aexit__(self, *args):
                    pass

            async def __call__(self, db_id):
                assert db_id == TEST_DB_ID
                return self.ConnMock(self)


            def is_all_tns_closed(self):
                for tn in self.tns:
                    if tn.state != 'closed':
                        return False
                return True

        self.env = MagicMock()
        self.env.app = MagicMock()
        self.env.app.db = DBMock()

        self.stream = TestStream(MagicMock())

    @asynctest
    async def test_list(self):
        test_items = [
            {
                'id': 'id1',
                'title': 'title1',
            },
            {
                'id': 'id2',
                'title': 'title2',
            },
        ]
        action = actions.List(self.stream)

        #test {}
        @with_transaction(self)
        async def count(conn, query):
            self.assert_compile(
                query,
                "SELECT test_table1.id FROM test_table1 "
                    "ORDER BY test_table1.id",
                literal_binds=True,
            )
            return 'TOTAL'
        self.stream.mapper.count = count

        @with_transaction(self)
        async def select(conn, ids=None, query=None, keys=None):
            self.assert_compile(
                query,
                "SELECT test_table1.id FROM test_table1 "
                   "ORDER BY test_table1.id LIMIT 1",
                literal_binds=True,
            )
            self.assertEqual(keys, {'id', 'title'})
            return test_items
        self.stream.mapper.select = select

        resp = await action.handle(self.env, {})
        self.assertEqual(resp['stream'], 'test_stream')
        self.assertEqual(resp['title'], 'test_stream_title')
        self.assertEqual(resp['action'], action.name)
        self.assertEqual(
            resp['list_fields'],
            ['ID_LIST_WIDGET', 'TITLE_LIST_WIDGET'],
        )
        self.assertEqual(resp['items'], [
            {
                'id': 'id1-from_python',
                'title': 'title1-from_python',
            },
            {
                'id': 'id2-from_python',
                'title': 'title2-from_python',
            },

        ])
        self.assertEqual(resp['total'], 'TOTAL')
        self.assertEqual(
            resp['filters_fields'],
            ['ID_FILTER_WIDGET', 'TITLE_FILTER_WIDGET', 'TITLE2_FILTER_WIDGET'],
        )
        self.assertEqual(resp['filters_errors'], {})
        self.assertEqual(resp['filters'], {})
        self.assertEqual(resp['page_size'], 1)
        self.assertEqual(resp['page'], 1)
        self.assertEqual(resp['order'], '+id')

        self.assertTrue(self.env.app.db_mock.is_all_tns_closed())

        #test all
        @with_transaction(self)
        async def count(conn, query):
            self.assert_compile(
                query,
                "SELECT test_table1.id FROM test_table1 "
                    "WHERE test_table1.id = 'id_filter-to_python' "
                    "AND test_table1.title = 'title_filter-to_python' "
                    "ORDER BY test_table1.title DESC",
                literal_binds=True,
            )
            return 'TOTAL'
        self.stream.mapper.count = count

        @with_transaction(self)
        async def select(conn, ids=None, query=None, keys=None):
            self.assert_compile(
                query,
                "SELECT test_table1.id FROM test_table1 "
                    "WHERE test_table1.id = 'id_filter-to_python' "
                    "AND test_table1.title = 'title_filter-to_python' "
                    "ORDER BY test_table1.title DESC "
                    "LIMIT 10 OFFSET 20",
                literal_binds=True,
            )
            self.assertEqual(keys, {'id', 'title'})
            return test_items
        self.stream.mapper.select = select

        resp = await action.handle(self.env, {
            'filters': {'id': 'id_filter', 'title': 'title_filter'},
            'order': '-title',
            'page': 3,
            'page_size': 10,
        })

        self.assertEqual(resp['stream'], 'test_stream')
        self.assertEqual(resp['title'], 'test_stream_title')
        self.assertEqual(resp['action'], action.name)
        self.assertEqual(
            resp['list_fields'],
            ['ID_LIST_WIDGET', 'TITLE_LIST_WIDGET'],
        )
        self.assertEqual(resp['items'], [
            {
                'id': 'id1-from_python',
                'title': 'title1-from_python',
            },
            {
                'id': 'id2-from_python',
                'title': 'title2-from_python',
            },

        ])
        self.assertEqual(resp['total'], 'TOTAL')
        self.assertEqual(
            resp['filters_fields'],
            ['ID_FILTER_WIDGET', 'TITLE_FILTER_WIDGET', 'TITLE2_FILTER_WIDGET'],
        )
        self.assertEqual(resp['filters_errors'], {})
        self.assertEqual(
                resp['filters'],
                {'id': 'id_filter', 'title': 'title_filter'},
        )
        self.assertEqual(resp['page_size'], 10)
        self.assertEqual(resp['page'], 3)
        self.assertEqual(resp['order'], '-title')
        # test MessageError
        self.stream.mapper.count = not_call
        self.stream.mapper.select = not_call

        with self.assertRaises(exc.MessageError):
            await action.handle(self.env, {
                'filters': 56,
           })
        with self.assertRaises(exc.MessageError):
            await action.handle(self.env, {
                'order': {},
           }) 
        with self.assertRaises(exc.MessageError):
            await action.handle(self.env, {
                'page': 'xxx',
           })
        with self.assertRaises(exc.MessageError):
            await action.handle(self.env, {
                'page_size': 'xxx',
           })
        with self.assertRaises(exc.MessageError):
            await action.handle(self.env, {
                'page': 0,
           })
        with self.assertRaises(exc.MessageError):
            await action.handle(self.env, {
                'page_size': -5,
           })
        with self.assertRaises(exc.StreamFieldNotFound):
            await action.handle(self.env, {
                'order': '+error_field',
           })
        with self.assertRaises(exc.MessageError):
            await action.handle(self.env, {
                'page_size': 100,
           })
        # test ValidationError
        @with_transaction(self)
        async def count(conn, query):
            self.assert_compile(
                query,
                "SELECT test_table1.id FROM test_table1 "
                    "WHERE test_table1.title = 'title_filter-to_python' "
                    "ORDER BY test_table1.id",
                literal_binds=True,
            )
            return 'TOTAL'
        self.stream.mapper.count = count

        @with_transaction(self)
        async def select(conn, ids=None, query=None, keys=None):
            self.assert_compile(
                query,
                "SELECT test_table1.id FROM test_table1 "
                    "WHERE test_table1.title = 'title_filter-to_python' "
                    "ORDER BY test_table1.id LIMIT 1",
                literal_binds=True,
            )
            return test_items
        self.stream.mapper.select = select

        resp = await action.handle(self.env, {
            'filters': {
                'id': exc.ValidationError,
                'title': 'title_filter',
            },
        })
        self.assertEqual(resp['filters_errors'], {'id': 'error'})
        self.assertEqual(
                resp['filters'],
                {'id': exc.ValidationError, 'title': 'title_filter'},
        )


    @asynctest
    async def test_get_item(self):
        action = actions.GetItem(self.stream)
        test_item = {
            'id': 'id1',
            'title': 'title1',
        }

        @with_transaction(self)
        async def select(conn, query, keys=None):
            self.assert_compile(
                query,
                "SELECT test_table1.id FROM test_table1 "
                    "WHERE test_table1.id = 500",
                literal_binds=True,
            )
            self.assertEqual(keys, None)
            return [test_item]
        self.stream.mapper.select = select

        resp = await action.handle(self.env, {'item_id': 500})
        self.assertEqual(
            resp['item_fields'],
            ['ID_ITEM_WIDGET', 'TITLE_ITEM_WIDGET'],
        )
        self.assertEqual(resp['item'], {
            'id': 'id1-from_python',
            'title': 'title1-from_python',
        })
        # test Errors
        self.stream.mapper.count = not_call
        self.stream.mapper.select = not_call

        with self.assertRaises(exc.MessageError):
            await action.handle(self.env, {
                'item_id': {},
            })
        with self.assertRaises(exc.MessageError):
            await action.handle(self.env, {})

        @with_transaction(self)
        async def select(conn, ids=None, query=None, keys=None):
            return []
        self.stream.mapper.select = select

        with self.assertRaises(exc.StreamItemNotFound):
            await action.handle(self.env, {'item_id': 500})

        @with_transaction(self)
        async def select(conn, ids=None, query=None, keys=None):
            return [1, 2]
        self.stream.mapper.select = select

        with self.assertRaises(AssertionError):
            await action.handle(self.env, {'item_id': 500})

    @asynctest
    async def test_new_item(self):
        action = actions.NewItem(self.stream)
        resp = await action.handle(self.env, {})
        self.assertEqual(
            resp['item_fields'],
            ['ID_ITEM_WIDGET', 'TITLE_ITEM_WIDGET'],
        )
        self.assertEqual(
            resp['item'],
            {
                'title': 'title-test_default-initials-from_python',
                'id': 'id-test_default-initials-from_python',
            },
        )

        resp = await action.handle(self.env,
            {'kwargs':{'test_kwarg': 'test_init'}})
        self.assertEqual(
            resp['item_fields'],
            ['ID_ITEM_WIDGET', 'TITLE_ITEM_WIDGET'],
        )
        self.assertEqual(
            resp['item'],
            {
                'title': 'title-test_init-initials-from_python',
                'id': 'id-test_init-initials-from_python',
            },
        )

        with self.assertRaises(exc.MessageError):
            await action.handle(self.env, {
                'kwargs': [],
           })

    @asynctest
    async def test_create_item(self):
        action = actions.CreateItem(self.stream)
        @with_transaction(self)
        async def insert(conn, item):
            new_item = item.copy()
            self.assertEqual(
                item,
                {'title': 'test_title-to_python'},
            )
            new_item['id'] = 123
            return new_item
        self.stream.mapper.insert = insert

        resp = await action.handle(self.env,
            {'values': {'title': 'test_title'}})

        self.assertEqual(
            resp['item_fields'],
            ['ID_ITEM_WIDGET', 'TITLE_ITEM_WIDGET'],
        )
        self.assertEqual(
            resp['item'],
            {
                'id': '123-from_python',
                'title': 'test_title-to_python-from_python',
            },
        )
        self.assertEqual(resp['errors'], {})

        @with_transaction(self)
        async def insert(conn, item):
            new_item = item.copy()
            self.assertEqual(
                item,
                {
                    'id': '123-to_python',
                    'title': 'test_title-to_python',
                },
            )
            return new_item
        self.stream.mapper.insert = insert

        resp = await action.handle(self.env,
            {'values': {'id': 123, 'title': 'test_title'}})

        self.assertEqual(
            resp['item_fields'],
            ['ID_ITEM_WIDGET', 'TITLE_ITEM_WIDGET'],
        )
        self.assertEqual(
            resp['item'],
            {
                'id': '123-to_python-from_python',
                'title': 'test_title-to_python-from_python',
            },
        )
        self.assertEqual(resp['errors'], {})

        # errors
        self.stream.mapper.insert = not_call

        with self.assertRaises(exc.MessageError):
            await action.handle(self.env, {})

        with self.assertRaises(exc.MessageError):
            await action.handle(self.env, {'values': []})

        with self.assertRaises(exc.MessageError):
            await action.handle(self.env, {'kwargs': None})


        resp = await action.handle(
            self.env,
            {'values': {'id': 123, 'title': exc.ValidationError}},
        )

        self.assertEqual(
            resp['item_fields'],
            ['ID_ITEM_WIDGET', 'TITLE_ITEM_WIDGET'],
        )
        self.assertEqual(
            resp['item'],
            {
                'id': 123,
                'title': exc.ValidationError,
            },
        )
        self.assertEqual(resp['errors'], {'title': 'error'})



        # id tests
        self.stream.item_fields = [
            item_fields.id,
        ]
        @with_transaction(self)
        async def insert(conn, item):
            new_item = item.copy()
            self.assertEqual(item, {})
            new_item['id'] = 123
            return new_item
        self.stream.mapper.insert = insert
        resp = await action.handle(self.env, {'values': {}})

        @with_transaction(self)
        async def insert(conn, item):
            new_item = item.copy()
            self.assertEqual(item, {'id': None})
            new_item['id'] = 123
            return new_item
        self.stream.mapper.insert = insert
        resp = await action.handle(self.env, {'values': {'id': None}})

        with self.assertRaises(exc.RawValueTypeError):
            resp = await action.handle(self.env, {'values': {'id': ''}})

        # test kwargs
        old_get_item_form = self.stream.get_item_form
        def get_item_form(env, kwargs):
            self.assertEqual(kwargs, {'test_kwarg': 'test'})
            return old_get_item_form(env, kwargs)
        self.stream.get_item_form=get_item_form
        resp = await action.handle(
            self.env,
            {'values': {'id': None}, 'kwargs': {'test_kwarg': 'test'}},
        )

    @asynctest
    async def test_update_item(self):
        action = actions.UpdateItem(self.stream)
        @with_transaction(self)
        async def update(conn, id, item, query=None, keys=None):
            self.assertEqual(id, 50)
            self.assertEqual(item, {'title': 'new_title-to_python'})
            self.assert_compile(
                query,
                "SELECT test_table1.id FROM test_table1",
                literal_binds=True,
            )
            self.assertEqual(keys, ['title'])
            return {
                'id': 50,
                'title': 'new_title',
            }
        self.stream.mapper.update = update
        resp = await action.handle(
            self.env,
            {
                'item_id': 50,
                'values': {'title': 'new_title'}
            }
        )
        self.assertEqual(resp['item_id'], 50)
        self.assertEqual(
            resp['item_fields'],
            ['ID_ITEM_WIDGET', 'TITLE_ITEM_WIDGET'],
        )
        self.assertEqual(
            resp['values'],
            {
                'id': '50-from_python',
                'title': 'new_title-from_python',
            },
        )
        self.assertEqual(resp['errors'], {})


        @with_transaction(self)
        async def update(conn, id, item, query=None, keys=None):
            self.assertEqual(id, 50)
            self.assertEqual(
                item,
                {'id': '51-to_python', 'title': 'new_title-to_python'},
            )
            self.assert_compile(
                query,
                "SELECT test_table1.id FROM test_table1",
                literal_binds=True,
            )
            self.assertEqual(set(keys), {'id', 'title'})
            return {
                'id': 51,
                'title': 'new_title',
            }

        self.stream.mapper.update = update
        resp = await action.handle(
            self.env,
            {
                'item_id': 50,
                'values': {'id': 51, 'title': 'new_title'}
            }
        )
        self.assertEqual(resp['item_id'], 50)
        self.assertEqual(
            resp['item_fields'],
            ['ID_ITEM_WIDGET', 'TITLE_ITEM_WIDGET'],
        )
        self.assertEqual(
            resp['values'],
            {
                'id': '51-from_python',
                'title': 'new_title-from_python',
            },
        )
        self.assertEqual(resp['errors'], {})
        # test errors
        self.stream.mapper.update = not_call
        with self.assertRaises(exc.MessageError):
            resp = await action.handle(
                self.env,
                {'values': {'id': 51, 'title': 'new_title'}},
            )
        with self.assertRaises(exc.MessageError):
            resp = await action.handle(self.env, {})
        with self.assertRaises(exc.MessageError):
            resp = await action.handle(self.env, {'item_id': 16})

        @with_transaction(self)
        async def update(conn, id, item, query=None, keys=None):
            raise exc.ItemNotFound
        self.stream.mapper.update = update
        with self.assertRaises(exc.StreamItemNotFound):
            resp = await action.handle(
                self.env,
                {
                    'item_id': 50,
                    'values': {'id': 51, 'title': 'new_title'},
                }
            )
        resp = await action.handle(
            self.env,
            {
                'item_id': 50,
                'values': {'id': 51, 'title': exc.ValidationError},
            }
        )
        self.assertEqual(resp['item_id'], 50)
        self.assertEqual(
            resp['item_fields'],
            ['ID_ITEM_WIDGET', 'TITLE_ITEM_WIDGET'],
        )
        self.assertEqual(
            resp['values'],
            {
                'id': 51,
                'title': exc.ValidationError,
            },
        )
        self.assertEqual(resp['errors'], {'title': 'error'})


    @asynctest
    async def test_delete_item(self):
        action = actions.DeleteItem(self.stream)
        @with_transaction(self)
        async def delete(conn, id, query=None):
            self.assertEqual(id, 50)
            self.assert_compile(
                query,
                "SELECT test_table1.id FROM test_table1",
                literal_binds=True,
            )
        self.stream.mapper.delete = delete

        resp = await action.handle(self.env, {'item_id': 50})
        self.assertEqual(resp['item_id'], 50)

        with self.assertRaises(exc.MessageError):
            await action.handle(self.env, {})

        invalid_values = [None, 'aaa', [], {}, set()]
        for value in invalid_values:
            with self.assertRaises(exc.MessageError):
                await action.handle(self.env, {'item_id': value})

        @with_transaction(self)
        async def delete(conn, id, query=None):
            raise exc.ItemNotFound()
        self.stream.mapper.delete = delete
        with self.assertRaises(exc.StreamItemNotFound):
            await action.handle(self.env, {'item_id': 500})

