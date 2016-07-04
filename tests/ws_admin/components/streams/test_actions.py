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
from tests.models import models1


TEST_DB_ID = 'test_db_id'

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
        async def count_by_query(conn, query):
            self.assertIsInstance(conn, self.env.app.db.ConnMock)
            self.assertEqual(conn.tn.state, 'begin')
            self.assert_compile(
                query,
                "SELECT test_table1.id FROM test_table1 "
                    "ORDER BY test_table1.id",
                literal_binds=True,
            )
            return 'TOTAL'
        self.stream.mapper.count_by_query = count_by_query

        async def select_by_query(conn, query, keys):
            self.assertIsInstance(conn, self.env.app.db.ConnMock)
            self.assertEqual(conn.tn.state, 'begin')
            self.assert_compile(
                query,
                "SELECT test_table1.id FROM test_table1 "
                   "ORDER BY test_table1.id LIMIT 1",
                literal_binds=True,
            )
            self.assertEqual(keys, {'id', 'title'})
            return test_items
        self.stream.mapper.select_by_query = select_by_query

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
        async def count_by_query(conn, query):
            self.assertIsInstance(conn, self.env.app.db.ConnMock)
            self.assertEqual(conn.tn.state, 'begin')
            self.assert_compile(
                query,
                "SELECT test_table1.id FROM test_table1 "
                    "WHERE test_table1.id = 'id_filter-to_python' "
                    "AND test_table1.title = 'title_filter-to_python' "
                    "ORDER BY test_table1.title DESC",
                literal_binds=True,
            )
            return 'TOTAL'
        self.stream.mapper.count_by_query = count_by_query

        async def select_by_query(conn, query, keys):
            self.assertIsInstance(conn, self.env.app.db.ConnMock)
            self.assertEqual(conn.tn.state, 'begin')
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
        self.stream.mapper.select_by_query = select_by_query

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
        async def count_by_query(conn, query):
            raise Exception()
        self.stream.mapper.count_by_query = count_by_query

        async def select_by_query(conn, query, keys):
            raise Exception()
        self.stream.mapper.select_by_query = select_by_query

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
        async def count_by_query(conn, query):
            self.assert_compile(
                query,
                "SELECT test_table1.id FROM test_table1 "
                    "WHERE test_table1.title = 'title_filter-to_python' "
                    "ORDER BY test_table1.id",
                literal_binds=True,
            )
            return 'TOTAL'
        self.stream.mapper.count_by_query = count_by_query

        async def select_by_query(conn, query, keys):
            self.assert_compile(
                query,
                "SELECT test_table1.id FROM test_table1 "
                    "WHERE test_table1.title = 'title_filter-to_python' "
                    "ORDER BY test_table1.id LIMIT 1",
                literal_binds=True,
            )
            return test_items
        self.stream.mapper.select_by_query = select_by_query

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

        async def select_by_query(conn, query, keys=None):
            self.assertIsInstance(conn, self.env.app.db.ConnMock)
            self.assertEqual(conn.tn.state, 'begin')

            self.assert_compile(
                query,
                "SELECT test_table1.id FROM test_table1 "
                    "WHERE test_table1.id = 500",
                literal_binds=True,
            )
            self.assertEqual(keys, None)
            return [test_item]
        self.stream.mapper.select_by_query = select_by_query

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
        async def count_by_query(conn, query):
            raise Exception()
        self.stream.mapper.count_by_query = count_by_query

        async def select_by_query(conn, query, keys):
            raise Exception()
        self.stream.mapper.select_by_query = select_by_query

        with self.assertRaises(exc.MessageError):
            await action.handle(self.env, {
                'item_id': {},
            })
        with self.assertRaises(exc.MessageError):
            await action.handle(self.env, {})

        async def select_by_query(conn, query, keys=None):
            return []
        self.stream.mapper.select_by_query = select_by_query

        with self.assertRaises(exc.StreamItemNotFound):
            await action.handle(self.env, {'item_id': 500})

        async def select_by_query(conn, query, keys=None):
            return [1, 2]
        self.stream.mapper.select_by_query = select_by_query

        with self.assertRaises(AssertionError):
            await action.handle(self.env, {'item_id': 500})


