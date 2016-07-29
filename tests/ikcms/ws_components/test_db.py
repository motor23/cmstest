import asyncio
from unittest import TestCase, skipIf
from unittest.mock import MagicMock

from sqlalchemy import sql
from iktomi.utils import cached_property
from ikcms.ws_components.db import component
from ikcms.utils.asynctests import asynctest
from ikcms.orm import mappers

from tests.cfg import cfg
from tests.models import models1, models2, metadata

try:
    import aiomysql
    mysql_skip = False
except ImportError:
    mysql_skip = True

try:
    raise ImportError
    import aiopg
    pg_skip = False
except ImportError:
    pg_skip = True


class SQLAComponentTestCase(TestCase):

    test_models = {
        'db1': models1,
        'db2': models2,
    }

    @skipIf(mysql_skip, 'Aiomysql not installed')
    @asynctest
    async def test_mysql(self):
        await self._db_test(cfg.MYSQL_URL)

    @skipIf(pg_skip, 'Aiopg not instaled')
    @asynctest
    async def test_postgress(self):
        await self._db_test(cfg.POSTGRESS_URL)

    async def _db_test(self, db_url):
        app = MagicMock()
        del app.db
        app.cfg.DATABASES = {
            'db1': db_url,
            'db2': db_url,
        }

        session_cls_mock = MagicMock()
        Component = component(
            mappers=mappers.Registry(metadata),
            session_cls=session_cls_mock,
        )
        db = await Component.create(app)
        self.assertEqual(set(db.engines.keys()), set(app.cfg.DATABASES.keys()))
        self.assertEqual(
            db.binds,
            {
                self.test_models['db1'].test_table1: db.engines['db1'],
                self.test_models['db2'].test_table2: db.engines['db2'],
            }
        )
        session = await db()
        self.assertEqual(session, session_cls_mock(db.engines, db.binds))
