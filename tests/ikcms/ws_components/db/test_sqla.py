import asyncio
from unittest import TestCase, skipIf
from unittest.mock import MagicMock

from sqlalchemy import sql
from ikcms.ws_components.db.sqla import component
from ikcms.utils.asynctests import asynctest

from tests.cfg import cfg
from tests.models import models1, models2


MYSQL_URL = getattr(cfg, 'MYSQL_URL', None)
POSTGRESS_URL = getattr(cfg, 'POSTGRESS_URL', None)


class SQLAComponentTestCase(TestCase):

    test_models = {
        'db1': models1,
        'db2': models2,
    }

    @skipIf(not MYSQL_URL, 'mysql url undefined')
    @asynctest
    async def test_mysql(self):
        await self._db_test(MYSQL_URL)

    @skipIf(not POSTGRESS_URL, 'mysql url undefined')
    @asynctest
    async def test_postgress(self):
        await self._db_test(POSTGRESS_URL)


    async def _db_test(self, db_url):
        app = MagicMock()
        del app.db
        app.cfg.DATABASES = {
            'db1': db_url,
            'db2': db_url,
        }

        def get_models(db_id):
            self.assertIn(db_id, app.cfg.DATABASES)
            return self.test_models[db_id]

        Component = component(get_models=get_models)

        db = await Component.create(app)
        self.assertEqual(db.models, self.test_models)
        engine1 = db.engines['db1']
        engine2 = db.engines['db2']
        self.assertEqual(db.binds[models1.test_table1], engine1)
        self.assertEqual(db.binds[models2.test_table2], engine2)
        test_table1 = self.test_models['db1'].test_table1
        async with await db('db1') as conn1:
            await self.test_models['db1'].reset(conn1)
            q = sql.insert(test_table1).values(id=5, title='test_title')
            result = await conn1.execute(q)
            self.assertEqual(result.lastrowid, 5)
            q = sql.select(test_table1.c).where(test_table1.c.id==5)
            result = await conn1.execute(q)
            self.assertEqual(result.rowcount, 1)
            result = list(result)
            self.assertEqual(result[0]['id'], 5)
            self.assertEqual(result[0]['title'], 'test_title')

            q = sql.update(test_table1).where(test_table1.c.id==5).\
                    values(title='test_title2')
            result = await conn1.execute(q)
            self.assertEqual(result.rowcount, 1)
            q = sql.select(test_table1.c).\
                    where(test_table1.c.id==5)
            result = await conn1.execute(q)
            self.assertEqual(result.rowcount, 1)
            result = list(result)
            self.assertEqual(result[0]['id'], 5)
            self.assertEqual(result[0]['title'], 'test_title2')

            q = sql.delete(test_table1).where(test_table1.c.id==5)
            result = await conn1.execute(q)
            self.assertEqual(result.rowcount, 1)
            q = sql.select(test_table1.c).\
                    where(test_table1.c.id==5)
            result = await conn1.execute(q)
            self.assertEqual(result.rowcount, 0)


