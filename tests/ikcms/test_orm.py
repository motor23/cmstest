from unittest import TestCase, skipIf
from unittest.mock import MagicMock

from sqlalchemy import sql


from ikcms.ws_components.db.sqla import component
from ikcms import orm
from ikcms.utils.asynctests import asynctest

from tests.cfg import cfg
from tests.models import models1


MYSQL_URL = getattr(cfg, 'MYSQL_URL', None)
POSTGRESS_URL = getattr(cfg, 'MYSQL_URL', None)
DB_URL = MYSQL_URL or POSTGRESS_URL


@skipIf(not DB_URL, 'db url undefined')
class MapperTestCase(TestCase):

    test_items = [
        {'id': 1, 'title': '111t', 'title2': '111t2'},
        {'id': 2, 'title': '222t', 'title2': '222t2'},
        {'id': 3, 'title': '333t', 'title2': '333t2'},
        {'id': 4, 'title': '444t', 'title2': '444t2'},
    ]
    models1 = models1


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mapper = orm.Mapper(self.models1.test_table1, {}, db_id='db1')

    async def create_db(self):
        app = MagicMock()
        del app.db
        app.cfg.DATABASES = {'db1': DB_URL}

        Component = component(
            get_models=MagicMock(return_value=self.models1),
        )

        db = await Component.create(app)
        async with await db('db1') as conn:
            await self.models1.reset(conn)
        return db

    def test_init(self):
        self.assertEqual(self.mapper.db_id, 'db1')
        self.assertEqual(self.mapper.table_keys, {'id', 'title', 'title2'})
        self.assertEqual(self.mapper.relation_keys, set())
        self.assertEqual(self.mapper.allowed_keys, {'id', 'title', 'title2'})

    def test_div_keys(self):
        table_keys, relation_keys = self.mapper.div_keys()
        self.assertEqual(table_keys, {'id', 'title', 'title2'})
        self.assertEqual(relation_keys, set())
        table_keys, relation_keys = self.mapper.div_keys(['title', 'title2'])
        self.assertEqual(table_keys, {'title', 'title2'})
        self.assertEqual(relation_keys, set())


    @asynctest
    async def test_select(self):
        db = await self.create_db()
        async with await db('db1') as conn:
            q = sql.insert(self.models1.test_table1).values(self.test_items)
            result = await conn.execute(q)

            items = await self.mapper.select_by_ids(conn, [4,2])
            self.assertEqual(items, [self.test_items[4-1], self.test_items[2-1]])
            items = await self.mapper.select_by_ids(conn, [4,2], keys=['title'])
            self.assertEqual(items, [
                {'id': 4, 'title': '444t'},
                {'id': 2, 'title': '222t'},
            ])

            q = self.mapper.query()
            q = q.where(self.mapper.table.c.title=='333t')
            items = await self.mapper.select_by_query(conn, q)
            self.assertEqual(items, [self.test_items[3-1]])
            items = await self.mapper.select_by_query(conn, q, keys=['title2'])
            self.assertEqual(items, [
                {'id': 3, 'title2': '333t2'},
            ])

            with self.assertRaises(orm.ItemNotFound) as e:
                await self.mapper.select_by_ids(conn, [4, 50, 2])
            self.assertEqual(e.exception.args[0], 50)

    @asynctest
    async def test_insert(self):
        db = await self.create_db()
        async with await db('db1') as conn:
            result = await self.mapper.insert(conn, self.test_items[3-1])
            self.assertEqual(result, self.test_items[3-1])
            result = await self.mapper.insert(conn, self.test_items[1-1])
            self.assertEqual(result, self.test_items[1-1])
            test_item4 = self.test_items[4-1].copy()
            test_item4['id'] = None
            result = await self.mapper.insert(conn, test_item4)
            self.assertEqual(result, self.test_items[4-1])
            with self.assertRaises(Exception):
                await self.mapper.insert(conn, self.test_items[3-1])

    @asynctest
    async def test_update(self):
        db = await self.create_db()
        async with await db('db1') as conn:
            q = sql.insert(self.models1.test_table1).values(self.test_items)
            result = await conn.execute(q)
            # test without 'keys' key arg
            updated_item2 = dict(self.test_items[2-1], title='updated')
            item = await self.mapper.update(conn, updated_item2)
            self.assertEqual(item, updated_item2)
            items = await self.mapper.select_by_ids(conn, [2])
            self.assertEqual(items, [updated_item2])
            items = await self.mapper.select_by_ids(conn, [1, 2, 3, 4])
            self.assertEqual(items, [
                self.test_items[1-1],
                updated_item2,
                self.test_items[3-1],
                self.test_items[4-1],
            ])
            # test with 'keys' key arg
            updated_item4 = dict(self.test_items[4-1], title2='updated2')
            item = await self.mapper.update(
                conn,
                {'id':4, 'title2': 'updated2'},
                ['title2'],
            )
            self.assertEqual(item, {'id':4, 'title2': 'updated2'})
            items = await self.mapper.select_by_ids(conn, [4])
            self.assertEqual(items, [updated_item4])
            items = await self.mapper.select_by_ids(conn, [1, 2, 3, 4])
            self.assertEqual(items, [
                self.test_items[1-1],
                updated_item2,
                self.test_items[3-1],
                updated_item4,
            ])

    @asynctest
    async def test_delete(self):
        db = await self.create_db()
        async with await db('db1') as conn:
            q = sql.insert(self.models1.test_table1).values(self.test_items)
            result = await conn.execute(q)
            item = await self.mapper.delete(conn, 2)
            with self.assertRaises(orm.ItemNotFound) as e:
                await self.mapper.select_by_ids(conn, [2])
            self.assertEqual(e.exception.args[0], 2)
            with self.assertRaises(orm.ItemNotFound) as e:
                await self.mapper.delete(conn, 2)
            self.assertEqual(e.exception.args[0], 2)
            items = await self.mapper.select_by_ids(conn, [1, 3, 4])
            self.assertEqual(items, [
                self.test_items[1-1],
                self.test_items[3-1],
                self.test_items[4-1],
            ])

