from unittest import TestCase
from unittest import skipIf
from unittest.mock import MagicMock
from datetime import date

from sqlalchemy import sql


from ikcms.ws_components.db import component
from ikcms import orm
from ikcms.orm import exc
from ikcms.utils.asynctests import asynctest

from tests.cfg import cfg
from tests.models import models1, models2, metadata


MYSQL_URL = getattr(cfg, 'MYSQL_URL', None)
POSTGRESS_URL = getattr(cfg, 'MYSQL_URL', None)
DB_URL = MYSQL_URL or POSTGRESS_URL


@skipIf(not DB_URL, 'db url undefined')
class BaseMapperTestCase(TestCase):

    item1 = {
            'id': 1,
            'title': '111t',
            'title2': '111t2',
            'date': date(2005, 4, 20),
    }
    item2 = {
            'id': 2,
            'title': '222t',
            'title2': '222t2',
            'date': date(1998, 7, 6),
    }
    item3 = {
            'id': 3,
            'title': '333t',
            'title2': '333t2',
            'date': date(2016, 12, 12),
    }
    item4 = {
            'id': 4,
            'title': '444t',
            'title2': '444t2',
            'date': date(2020, 1, 17),
    }
    items = [item1, item2, item3, item4]
    items_table_keys = {'id', 'title', 'title2', 'date'}
    items_relation_keys = set()
    items_allowed_keys = items_table_keys.union(items_relation_keys)
    models1 = models1
    models2 = models2
    mapper_cls = orm.mappers.Base

    async def asetup(self):
        registry = orm.mappers.Registry(metadata)
        self.mapper_cls.from_model(registry, 'Test', [self.models1.Test])

        app = MagicMock()
        del app.db
        app.cfg.DATABASES = {
            'db1': DB_URL,
            'db2': DB_URL,
        }

        Component = component(mappers=registry)

        db = await Component.create(app)
        async with await db() as session:
            conn1 = await session.get_connection(db.engines['db1'])
            await self.models1.reset(conn1)
            conn2 = await session.get_connection(db.engines['db2'])
            await self.models2.reset(conn2)
        return {
            'db': db,
        }

    async def aclose(self, db):
        db.close()

    @asynctest
    async def test_init(self, db):
        mapper = db.mappers['db1']['Test']
        self.assertEqual(mapper.registry, db.mappers)
        self.assertEqual(mapper.db_id, 'db1')
        self.assertEqual(mapper.table_keys, self.items_table_keys)
        self.assertEqual(mapper.relation_keys, self.items_relation_keys)
        self.assertEqual(mapper.allowed_keys, self.items_allowed_keys)

    @asynctest
    async def test_div_keys(self, db):
        mapper = db.mappers['db1']['Test']
        table_keys, relation_keys = mapper.div_keys()
        self.assertEqual(table_keys, self.items_table_keys)
        self.assertEqual(relation_keys, self.items_relation_keys)
        table_keys, relation_keys = mapper.div_keys(['title', 'title2'])
        self.assertEqual(table_keys, {'title', 'title2'})
        self.assertEqual(relation_keys, set())


    @asynctest
    async def test_select(self, db):
        mapper = db.mappers['db1']['Test']
        query = mapper.query()
        async with await db() as session:
            q = sql.insert(self.models1.test_table1).values(self.items)
            result = await session.execute(q)

            # ids arg
            items = await query.id(2, 4).select_items(session)
            self.assertEqual(items, [self.item2, self.item4])
            items = await query.id(2, 4).select_items(session, keys=['title'])
            self.assertEqual(items, [
                {'id': 2, 'title': '222t'},
                {'id': 4, 'title': '444t'},
            ])

            # query arg
            _query = query.filter_by(title='333t')
            items = await _query.select_items(session)
            self.assertEqual(items, [self.item3])

            items = await _query.select_items(session, keys=['title2'])
            self.assertEqual(items, [{'id': 3, 'title2': '333t2'}])

            # ids and query args
            items = await query.id(4,2).select_items(session)
            self.assertEqual(items, [self.item2, self.item4])

            _query = query.filter_by(title='333t').id(44)
            items = await _query.select_items(session)
            self.assertEqual(items, [])

    @asynctest
    async def test_insert(self, db):
        mapper = db.mappers['db1']['Test']
        _item1 = dict(self.item1, title2=None, date=None)
        _item4 = dict(self.item4, id=None)

        query = mapper.query().order_by(mapper.c['id'])
        async with await db() as session:
            result = await query.insert_item(session, self.item3)
            self.assertEqual(result, self.item3)
            items = await query.select_items(session)
            self.assertEqual(items, [self.item3])

            result = await query.insert_item(
                session, self.item1, keys=['id', 'title'])
            self.assertEqual(result, self.item1)
            items = await query.select_items(session)
            self.assertEqual(items, [_item1, self.item3])

            result = await query.insert_item(session, _item4)
            self.assertEqual(result, self.item4)
            items = await query.select_items(session)
            self.assertEqual(items, [_item1, self.item3, self.item4])

            with self.assertRaises(Exception): # XXX Exception??
                await mapper.insert_item(session, item3)

    @asynctest
    async def test_update(self, db):
        mapper = db.mappers['db1']['Test']
        query = mapper.query().order_by(mapper.c['id'])
        async with await db() as session:
            q = sql.insert(self.models1.test_table1).values(self.items)
            result = await session.execute(q)
            # test without 'keys' key arg
            _item2 = dict(self.item2, title='updated')
            item = await query.update_item(session, 2, _item2)
            self.assertEqual(item, _item2)
            items = await query.id(2).select_items(session)
            self.assertEqual(items, [_item2])
            items = await query.id(1, 2, 3, 4).select_items(session)
            self.assertEqual(items, [
                self.item1,
                _item2,
                self.item3,
                self.item4,
            ])
            # test with 'keys' key arg
            _item4 = dict(self.item4, title2='updated2')
            item = await query.update_item(
                session,
                4,
                {'title2': 'updated2'},
                keys = ['title2'],
            )
            self.assertEqual(item, {'id':4, 'title2': 'updated2'})
            items = await query.id(4).select_items(session)
            self.assertEqual(items, [_item4])
            items = await query.id(1, 2, 3, 4).select_items(session)
            self.assertEqual(items, [
                self.item1,
                _item2,
                self.item3,
                _item4,
            ])
            query = query.filter_by(title='zzz')
            with self.assertRaises(exc.ItemNotFoundError) as e:
                await query.update_item(
                    session,
                    4,
                    {'id':4, 'title2': 'updated2'},
                    keys=['title2'],
                )
                self.assertEqual(e.args[0], 4)

    @asynctest
    async def test_delete(self, db):
        mapper = db.mappers['db1']['Test']
        query = mapper.query().order_by(mapper.c['id'])
        async with await db() as session:
            q = sql.insert(self.models1.test_table1).values(self.items)
            result = await session.execute(q)
            # id arg
            await query.delete_item(session, 2)
            self.assertEqual(await query.id(2).select_items(session), [])
            with self.assertRaises(exc.ItemNotFoundError) as e:
                await query.delete_item(session, 2)
            self.assertEqual(e.exception.args[0], 2)
            items = await query.id(1, 3, 4).select_items(session)
            self.assertEqual(items, [self.item1, self.item3, self.item4])
            _query = query.filter_by(title='zzz').id(4)
            items = await _query.select_items(session)
            self.assertEqual(items, [])

            await query.delete_item(session, 4)
            items = await query.select_items(session)
            self.assertEqual(items, [self.item1,  self.item3])

    @asynctest
    async def test_count(self, db):
        mapper = db.mappers['db1']['Test']
        query = mapper.query()
        async with await db() as session:
            result = await query.count_items(session)
            self.assertEqual(result, 0)

            q = sql.insert(self.models1.test_table1).values(self.items)
            await session.execute(q)
            result = await query.count_items(session)
            self.assertEqual(result, len(self.items))
            result = await query.filter_by(id=1).count_items(session)
            self.assertEqual(result, 1)

