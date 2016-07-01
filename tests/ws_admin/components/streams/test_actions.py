import asyncio
from unittest import TestCase
from unittest.mock import MagicMock

from ws_admin.components.streams import actions
from ws_admin.components.streams import exc

from ikcms.utils.asynctests import asynctest
from ws_admin.components.streams.stream import Stream


TEST_DB_ID = 'test_db_id'

class ActionsTestCase(TestCase):


    def setUp(self):
        class QueryMock:

            def __init__(self):
                self._conditions = []
                self._order = []
                self._limit = None
                self._offset = None

            def where(self, condition):
                self._conditions.append(condition)
                return self
            def limit(self, limit):
                self._limit = limit
                return self
            def offset(self, offset):
                self._offset = offset
                return self
            def order_by(self, order):
                self._order.append(order)
                return self


        class ModelFieldMock:
            def __init__(self, **kwargs):
                self.__dict__.update(kwargs)

            def desc(self):
                return (self.name, '-')


        class FormFieldMock:
            enable_order = False
            enable_filter = False
            _widget = None

            def __init__(self, **kwargs):
                self.__dict__.update(kwargs)

            def __call__(self, *args, **kwargs):
                return self

            def to_python(self, values):
                value = values.get(self.name)
                if value is not None:
                    if value==exc.ValidationError:
                        raise value({self.name: 'error'})
                    return {self.name: ('to_python', value)}
                else:
                    return {}

            def from_python(self, value):
                return {self.name: ('from_python', value.get(self.name))}

            def order(self, query, value):
                assert self.enable_order
                if value:
                    return query.order_by((self.name, value))

            def filter(self, query, value):
                assert self.enable_filter
                if value is not None:
                    query = query.where((self.name, value))
                return query

            @property
            def widget(self):
                return MagicMock(to_dict=MagicMock(return_value=self._widget))


        class TestStream(Stream):
            max_limit = 50
            name = 'test_stream'
            title = 'test_stream_title'
            mapper = MagicMock()
            mapper.db_id = TEST_DB_ID
            mapper.table.c = {
                'id': ModelFieldMock(name='id'),
                'title': ModelFieldMock(name='title'),
            }

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
                    FormFieldMock(name='id'),
                    FormFieldMock(name='title'),
            ]

            def query(self):
                return QueryMock()


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
            self.assertEqual(query._conditions, [])
            self.assertEqual(query._order, [('id', '+')])
            self.assertEqual(query._limit, None)
            self.assertEqual(query._offset, None)
            return 'TOTAL'
        self.stream.mapper.count_by_query = count_by_query

        async def select_by_query(conn, query, keys):
            self.assertIsInstance(conn, self.env.app.db.ConnMock)
            self.assertEqual(conn.tn.state, 'begin')
            self.assertEqual(query._conditions, [])
            self.assertEqual(query._order, [('id', '+')])
            self.assertEqual(query._limit, 1)
            self.assertEqual(query._offset, 0)
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
                'id': ('from_python', 'id1'),
                'title': ('from_python', 'title1'),
            },
            {
                'id': ('from_python', 'id2'),
                'title': ('from_python', 'title2'),
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
            self.assertEqual(
                query._conditions,
                [
                    ('id', ('to_python', 'id_filter')),
                    ('title', ('to_python', 'title_filter')),
                ]
            )
            self.assertEqual(query._order, [('title', '-')])
            self.assertEqual(query._limit, None)
            self.assertEqual(query._offset, None)
            return 'TOTAL'
        self.stream.mapper.count_by_query = count_by_query

        async def select_by_query(conn, query, keys):
            self.assertIsInstance(conn, self.env.app.db.ConnMock)
            self.assertEqual(conn.tn.state, 'begin')
            self.assertEqual(
                query._conditions,
                [
                    ('id', ('to_python', 'id_filter')),
                    ('title', ('to_python', 'title_filter')),
                ],
            )
            self.assertEqual(query._order, [('title', '-')])
            self.assertEqual(query._limit, 10)
            self.assertEqual(query._offset, 20)
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
                'id': ('from_python', 'id1'),
                'title': ('from_python', 'title1'),
            },
            {
                'id': ('from_python', 'id2'),
                'title': ('from_python', 'title2'),
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
            self.assertEqual(
                query._conditions,
                [('title', ('to_python', 'title_filter'))],
            )
            return 'TOTAL'
        self.stream.mapper.count_by_query = count_by_query

        async def select_by_query(conn, query, keys):
            self.assertEqual(
                query._conditions,
                [('title', ('to_python', 'title_filter'))],
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

