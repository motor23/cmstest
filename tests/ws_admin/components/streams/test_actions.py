import asyncio
from unittest import TestCase
from unittest import skipIf
from unittest.mock import MagicMock
from sqlalchemy import sql
#from sqlalchemy.testing.assertions import AssertsCompiledSQL

from ws_admin.components.streams import actions
from ws_admin.components.streams import exc

from ikcms import orm
from ikcms.utils.asynctests import asynctest
import ikcms.ws_components.db

from ws_admin.components.streams.stream import Stream
from ws_admin.components.streams.forms import list_fields
from ws_admin.components.streams.forms import filter_fields
from ws_admin.components.streams.forms import item_fields
from ikcms.forms.widgets import Widget

from tests.models import models1, models2, metadata
from tests.cfg import cfg


MYSQL_URL = getattr(cfg, 'MYSQL_URL', None)
POSTGRESS_URL = getattr(cfg, 'POSTGRESS_URL', None)
DB_URL = MYSQL_URL or POSTGRESS_URL

@skipIf(not DB_URL, 'db url undefined')
class ActionsTestCase(TestCase):
    test_items = [
        {'id': 1, 'title': '4-111t', 'title2': '111t2'},
        {'id': 2, 'title': '3-222t', 'title2': '222t2'},
        {'id': 3, 'title': '2-333t', 'title2': '333t2'},
        {'id': 4, 'title': '1-444t', 'title2': '444t2'},
    ]

    test_edit_items = test_list_items = [
        {'id': 1, 'title': '4-111t'},
        {'id': 2, 'title': '3-222t'},
        {'id': 3, 'title': '2-333t'},
        {'id': 4, 'title': '1-444t'},
    ]

    models1 = models1
    models2 = models2
    mapper_cls = orm.mappers.Base

    async def asetup(self):
        registry = orm.mappers.Registry(metadata)
        self.mapper_cls.from_model(registry, 'Test', [self.models1.Test])

        app = MagicMock()
        app.cfg.DATABASES = {
            'db1': DB_URL,
            'db2': DB_URL,
        }
        del app.db
        db = await ikcms.ws_components.db.component(mappers=registry).create(app)
        async with await db() as session:
            conn1 = await session.get_connection(db.engines['db1'])
            await self.models1.reset(conn1)
            conn2 = await session.get_connection(db.engines['db2'])
            await self.models2.reset(conn2)

        class l_id(list_fields.id):
            widget = MagicMock()

        class l_title(list_fields.title):
            widget = MagicMock()

        class f_id(filter_fields.id):
            widget = MagicMock()

        class f_title(filter_fields.title):
            widget = MagicMock()

        class f_title2(filter_fields.title):
            name = 'title2'
            title = 'title2'
            widget = MagicMock()

        class i_id(item_fields.id):
            widget = MagicMock()

            def get_initials(_self, test_kwarg='test_default'):
                return '{}-{}-initials'.format(_self.name, test_kwarg)

        class i_title(item_fields.title):
            widget = MagicMock()

            def get_initials(_self, test_kwarg='test_default'):
                return '{}-{}-initials'.format(_self.name, test_kwarg)

        class TestStream(Stream):
            max_limit = 50
            name = 'test_stream'
            title = 'test_stream_title'
            mapper = registry['db1']['Test']

            list_fields = [
                l_id,
                l_title,
            ]
            filter_fields = [
                f_id,
                f_title,
                f_title2,
            ]
            item_fields = [
                i_id,
                i_title,
            ]

        stream = TestStream(MagicMock())
        env = MagicMock()
        env.app = app

        return {
            'db': db,
            'stream': stream,
            'env': env,
        }

    async def aclose(self, db, stream, env):
        db.close()


    def _base_assert_list_action_response(self, resp, action, stream):
        self.assertEqual(resp['stream'], 'test_stream')
        self.assertEqual(resp['title'], 'test_stream_title')
        self.assertEqual(resp['action'], action.name)
        self.assertEqual(
            resp['list_fields'],
            [f.widget.to_dict(f) for f in stream.list_fields],
        )
        self.assertEqual(
            resp['filters_fields'],
            [f.widget.to_dict(f) for f in stream.filter_fields],
        )


    @asynctest
    async def test_list(self, db, stream, env):
        action = actions.List(stream)
        mapper = db.mappers['db1']['Test']
        async with await db() as session:
            q = sql.insert(self.models1.test_table1).values(self.test_items)
            result = await session.execute(q)

        list_item1 = {'id': 1, 'title': '4-111t'}
        list_item2 = {'id': 2, 'title': '3-222t'}
        list_item3 = {'id': 3, 'title': '2-333t'}
        list_item4 = {'id': 4, 'title': '1-444t'}
        list_items = [list_item1, list_item2, list_item3, list_item4]
        list_items_desc = list_items[::-1]

        # test order
        order_values = [
            (None, list_items),
            ('+id', list_items),
            ('-title', list_items),
            ('+title', list_items[::-1]),
        ]
        filters_values = [
            (None, lambda i: True),
            ({}, lambda i: True),
        ]
        for id in [-5, 0, 1, 3, 10]:
            def func(x):
                return lambda i:i['id']==x
            filters_values.append(({'id': id}, func(id)))
        for title in ['1', 't', '2-333t', '24']:
            def func(x):
                return lambda i:i['title'].find(x)!=-1
            filters_values.append(({'title': title}, func(title)))
        for order, items in order_values:
            _order = order or '+id'
            for filters, filter_func in filters_values:
                _filters = filters or {}
                _items = list(filter(filter_func, items))
                for page_size in [None, 1, 3, 4, 50]:
                    _page_size = page_size or 1
                    for page in [None, 1, 2, 3, 4, 10]:
                        _page = page or 1

                        kwargs = {}
                        if order is not None:
                            kwargs['order'] = order
                        if filters is not None:
                            kwargs['filters'] = filters
                        if page_size is not None:
                            kwargs['page_size'] = page_size
                        if page is not None:
                            kwargs['page'] = page

                        resp = await action.handle(env, kwargs)
                        self._base_assert_list_action_response(
                            resp, action, stream)
                        self.assertEqual(
                            resp['items'],
                            _items[(_page-1)*_page_size:_page*_page_size],
                        )
                        self.assertEqual(resp['filters_errors'], {})
                        self.assertEqual(resp['filters'], _filters)
                        self.assertEqual(resp['page_size'], _page_size)
                        self.assertEqual(resp['page'], _page)
                        self.assertEqual(resp['order'], _order)
                        self.assertEqual(resp['total'], len(_items))


        error_page_values = [-10, 0, 5.6, 'aaaa', '20', None]
        for value in error_page_values:
            with self.assertRaises(exc.MessageError):
                await action.handle(env, {
                    'page': value,
               })
        error_page_size_values = [-10, 0, 5.6, 'aaa', '20', None]
        for value in error_page_size_values:
            with self.assertRaises(exc.MessageError):
                await action.handle(env, {
                    'page': value,
               })

        with self.assertRaises(exc.MessageError):
            await action.handle(env, {
                'filters': 56,
           })
        with self.assertRaises(exc.MessageError):
            await action.handle(env, {
                'order': {},
           }) 
        with self.assertRaises(exc.MessageError):
            await action.handle(env, {
                'page': 'xxx',
           })
        with self.assertRaises(exc.MessageError):
            await action.handle(env, {
                'page_size': 'xxx',
           })
        with self.assertRaises(exc.MessageError):
            await action.handle(env, {
                'page_size': -5,
           })
        with self.assertRaises(exc.StreamFieldNotFound):
            await action.handle(env, {
                'order': '+error_field',
           })
        with self.assertRaises(exc.MessageError):
            await action.handle(env, {
                'page_size': 100,
           })

        #XXX to do: test ValidationError


    @asynctest
    async def test_get_item(self, db, stream, env):
        action = actions.GetItem(stream)
        mapper = db.mappers['db1']['Test']
        async with await db() as session:
            q = sql.insert(self.models1.test_table1).values(self.test_items)
            result = await session.execute(q)


        for item in self.test_edit_items:
            resp = await action.handle(env, {'item_id': item['id']})
            self.assertEqual(
                resp['item_fields'],
                [f.widget.to_dict(f) for f in stream.item_fields],
            )
            self.assertEqual(resp['item'], item)

        for value in [-10, 0, 5, 500]:
            with self.assertRaises(exc.StreamItemNotFound):
                await action.handle(env, {'item_id': value})

        with self.assertRaises(exc.MessageError):
            await action.handle(env, {})

        for value in [{}, None, [1,2]]:
            with self.assertRaises(exc.MessageError):
                await action.handle(env, {'item_id': value})


    @asynctest
    async def test_new_item(self, db, stream, env):
        action = actions.NewItem(stream)

        resp = await action.handle(env, {})
        self.assertEqual(
            resp['item_fields'],
            [f.widget.to_dict(f) for f in stream.item_fields],
        )
        self.assertEqual(resp['item'],
            {
                'title': 'title-test_default-initials',
                'id': 'id-test_default-initials',
            },
        )


        resp = await action.handle(env,
            {'kwargs':{'test_kwarg': 'test_init'}})
        self.assertEqual(
            resp['item_fields'],
            [f.widget.to_dict(f) for f in stream.item_fields],
        )
        self.assertEqual(resp['item'],
            {
                'title': 'title-test_init-initials',
                'id': 'id-test_init-initials',
            },
        )

        for value in [None, 'xxx', [], 10]:
            with self.assertRaises(exc.MessageError):
                await action.handle(env, {
                    'kwargs': value,
               })

    @asynctest
    async def test_create_item(self, db, stream, env):
        mapper = db.mappers['db1']['Test']
        action = actions.CreateItem(stream)
        items = [
            {'id':1, 'title': 'test_title-1'},
            {'id':2, 'title': 'test_title-2'},
            {'id':3, 'title': 'test_title-3'},
            {'id':10, 'title': 'test_title-10'},
            {'id':30, 'title': 'test_title-30'},
            {'id':121, 'title': 'test_title-121'},
        ]
        for item in items[:3]:
            resp = await action.handle(
                env,
                {'values': {'title': item['title']}}
            )
            self.assertEqual(
                resp['item_fields'],
                [f.widget.to_dict(f) for f in stream.item_fields],
            )
            self.assertEqual(resp['item'], item)
            self.assertEqual(resp['errors'], {})

        for item in items[3:]:
            resp = await action.handle(env, {'values': item})
            self.assertEqual(
                resp['item_fields'],
                [f.widget.to_dict(f) for f in stream.item_fields],
            )
            self.assertEqual(resp['item'], item)
            self.assertEqual(resp['errors'], {})

        async with await db() as session:
            q = sql.select([
                self.models1.test_table1.c.id,
                self.models1.test_table1.c.title,
            ]).order_by(self.models1.test_table1.c.id)
            result = await session.execute(q)
            result = [dict(row) for row in result]
            self.assertEqual(result, items)

        # errors
        with self.assertRaises(exc.MessageError):
            await action.handle(env, {})

        with self.assertRaises(exc.MessageError):
            await action.handle(env, {'values': []})

        with self.assertRaises(exc.MessageError):
            await action.handle(env, {'kwargs': None})

        # XXX raises RawValueTypeError
        #with self.assertRaises(exc.MessageError):
        #    resp = await action.handle(env, {'values': {'id': ''}})

        #XXX to do: test kwargs
        #XXX to do: test ValidationError

    @asynctest
    async def test_update_item(self, db, stream, env):
        action = actions.UpdateItem(stream)
        mapper = db.mappers['db1']['Test']
        async with await db() as session:
            q = sql.insert(self.models1.test_table1).values(self.test_items)
            result = await session.execute(q)
        result_items = self.test_edit_items.copy()

        resp = await action.handle(
            env,
            {
                'item_id': 3,
                'values': {'title': 'updated_title'}
            }
        )
        self.assertEqual(resp['item_id'], 3)
        self.assertEqual(
            resp['item_fields'],
            [f.widget.to_dict(f) for f in stream.item_fields],
        )
        self.assertEqual(
            resp['values'],
            {
                'id': 3,
                'title': 'updated_title',
            },
        )
        self.assertEqual(resp['errors'], {})
        result_items[3-1] = dict(result_items[3-1], title='updated_title')


        resp = await action.handle(
            env,
            {
                'item_id': 4,
                'values': {'id': 50, 'title': 'updated_title2'}
            }
        )
        self.assertEqual(resp['item_id'], 50)
        self.assertEqual(
            resp['item_fields'],
            [f.widget.to_dict(f) for f in stream.item_fields],
        )
        self.assertEqual(
            resp['values'],
            {
                'id': 50,
                'title': 'updated_title2',
            },
        )
        self.assertEqual(resp['errors'], {})
        result_items[4-1] = dict(
            result_items[4-1], id=50, title='updated_title2')

        async with await db() as session:
            q = sql.select([
                self.models1.test_table1.c.id,
                self.models1.test_table1.c.title,
            ]).order_by(self.models1.test_table1.c.id)
            result = await session.execute(q)
            result = [dict(row) for row in result]
            self.assertEqual(result, result_items)

        # test errors
        with self.assertRaises(exc.MessageError):
            resp = await action.handle(env, {})
        with self.assertRaises(exc.MessageError):
            resp = await action.handle(env, {'item_id': 16})

        with self.assertRaises(exc.StreamItemNotFound):
            resp = await action.handle(
                env,
                {
                    'item_id': 11,
                    'values': {'id': 51, 'title': 'new_title'},
                }
            )
        #XXX TO DO: ValidationError, RawTypeError


    @asynctest
    async def test_delete_item(self, db, stream, env):
        action = actions.DeleteItem(stream)
        mapper = db.mappers['db1']['Test']
        async with await db() as session:
            q = sql.insert(self.models1.test_table1).values(self.test_items)
            result = await session.execute(q)


        resp = await action.handle(env, {'item_id': 3})
        self.assertEqual(resp['item_id'], 3)

        with self.assertRaises(exc.MessageError):
            await action.handle(env, {})

        invalid_values = [None, 'aaa', [], {}, set()]
        for value in invalid_values:
            with self.assertRaises(exc.MessageError):
                await action.handle(env, {'item_id': value})

        with self.assertRaises(exc.StreamItemNotFound):
            await action.handle(env, {'item_id': 500})

        #XXX TO_DO: sql check, RawTypeError



