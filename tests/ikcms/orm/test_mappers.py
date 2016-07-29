from unittest import TestCase
from unittest import skipIf
from unittest.mock import MagicMock

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

    test_items = [
        {'id': 1, 'title': '111t', 'title2': '111t2'},
        {'id': 2, 'title': '222t', 'title2': '222t2'},
        {'id': 3, 'title': '333t', 'title2': '333t2'},
        {'id': 4, 'title': '444t', 'title2': '444t2'},
    ]
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
        self.assertEqual(mapper.table_keys, {'id', 'title', 'title2'})
        self.assertEqual(mapper.relation_keys, set())
        self.assertEqual(mapper.allowed_keys, {'id', 'title', 'title2'})

    @asynctest
    async def test_div_keys(self, db):
        mapper = db.mappers['db1']['Test']
        table_keys, relation_keys = mapper.div_keys()
        self.assertEqual(table_keys, {'id', 'title', 'title2'})
        self.assertEqual(relation_keys, set())
        table_keys, relation_keys = mapper.div_keys(['title', 'title2'])
        self.assertEqual(table_keys, {'title', 'title2'})
        self.assertEqual(relation_keys, set())


    @asynctest
    async def test_select(self, db):
        mapper = db.mappers['db1']['Test']
        async with await db() as session:
            q = sql.insert(self.models1.test_table1).values(self.test_items)
            result = await session.execute(q)

            # ids arg
            items = await mapper.query().id(2, 4).select_items(session)
            self.assertEqual(items, [
                self.test_items[2-1],
                self.test_items[4-1],
            ])
            return
            items = await self.mapper.select(conn, [2, 4], keys=['title'])
            self.assertEqual(items, [
                {'id': 2, 'title': '222t'},
                {'id': 4, 'title': '444t'},
            ])

            with self.assertRaises(orm.ItemNotFound) as e:
                await mapper.query().ids(4, 50, 2).items_select(session)
            self.assertEqual(e.exception.args[0], 50)

            # query arg
            query = mapper.query().filter_by(title='333t')
            items = await query.select_items(session)
            self.assertEqual(items, [self.test_items[3-1]])

            items = await query.select_items(sessions, keys=['title2'])
            self.assertEqual(items, [{'id': 3, 'title2': '333t2'}])

            # ids and query args
            query = self.mapper.query().id(4,2)
            items = await query.select_items(session)
            self.assertEqual(items, [self.test_items[4-1], self.test_items[2-1]])

            query = mapper.query().filter_by(title=='333t').id(4)
            with self.assertRaises(exc.ItemNotFound) as e:
                await query.select_items(session)
            self.assertEqual(e.exception.args[0], 4)

    @asynctest
    async def test_insert(self, db):
        mapper = db.mappers['db1']['Test']
        item1 = self.test_items[1-1]
        item1_ = dict(item1, title2=None)
        item3 = self.test_items[3-1]
        item4 = self.test_items[4-1]
        item4_ = dict(self.test_items[4-1], id=None)

        query = mapper.query().order_by(mapper.c['id'])
        async with await db() as session:
            result = await query.insert_item(session, item3)
            self.assertEqual(result, item3)
            items = await query.select_items(session)
            self.assertEqual(items, [item3])

            result = await query.insert_item(
                session, item1, keys=['id', 'title'])
            self.assertEqual(result, item1)
            items = await query.select_items(session)
            self.assertEqual(items, [item1_, item3])

            result = await query.insert_item(session, item4_)
            self.assertEqual(result, item4)
            items = await query.select_items(session)
            self.assertEqual(items, [item1_, item3, item4])

            with self.assertRaises(Exception):
                await mapper.insert_item(session, item3)

    @asynctest
    async def test_update(self, db):
        mapper = db.mappers['db1']['Test']
        query = mapper.query().order_by(mapper.c['id'])
        async with await db() as session:
            q = sql.insert(self.models1.test_table1).values(self.test_items)
            result = await session.execute(q)
            # test without 'keys' key arg
            updated_item2 = dict(self.test_items[2-1], title='updated')
            item = await query.update_item(session, 2, updated_item2)
            self.assertEqual(item, updated_item2)
            items = await query.id(2).select_items(session)
            self.assertEqual(items, [updated_item2])
            items = await query.id(1, 2, 3, 4).select_items(session)
            self.assertEqual(items, [
                self.test_items[1-1],
                updated_item2,
                self.test_items[3-1],
                self.test_items[4-1],
            ])
            # test with 'keys' key arg
            updated_item4 = dict(self.test_items[4-1], title2='updated2')
            item = await query.update_item(
                session,
                4,
                {'id':4, 'title2': 'updated2'},
                keys = ['title2'],
            )
            self.assertEqual(item, {'id':4, 'title2': 'updated2'})
            items = await query.id(4).select_items(session)
            self.assertEqual(items, [updated_item4])
            items = await query.id(1, 2, 3, 4).select_items(session)
            self.assertEqual(items, [
                self.test_items[1-1],
                updated_item2,
                self.test_items[3-1],
                updated_item4,
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
            q = sql.insert(self.models1.test_table1).values(self.test_items)
            result = await session.execute(q)
            # id arg
            await query.delete_item(session, 2)
            self.assertEqual(await query.id(2).select_items(session), [])
            with self.assertRaises(exc.ItemNotFoundError) as e:
                await query.delete_item(session, 2)
            self.assertEqual(e.exception.args[0], 2)
            items = await query.id(1, 3, 4).select_items(session)
            self.assertEqual(items, [
                self.test_items[1-1],
                self.test_items[3-1],
                self.test_items[4-1],
            ])
            q = query.filter_by(title='zzz').id(4)
            self.assertEqual(await q.select_items(session), [])

            await query.delete_item(session, 4)
            items = await query.select_items(session)
            self.assertEqual(items, [
                self.test_items[1-1],
                self.test_items[3-1],
            ])

    @asynctest
    async def test_count(self, db):
        mapper = db.mappers['db1']['Test']
        query = mapper.query()
        async with await db() as session:
            result = await query.count_items(session)
            self.assertEqual(result, 0)

            q = sql.insert(self.models1.test_table1).values(self.test_items)
            await session.execute(q)
            result = await query.count_items(session)
            self.assertEqual(result, 4)
            query = query.filter_by(id=1)
            result = await query.count_items(session)
            self.assertEqual(result, 1)

