from unittest import TestCase, skipIf
from unittest.mock import MagicMock

from sqlalchemy import sql
from ikcms.components.db.sqla import component

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
    def test_mysql(self):
        self._db_test(MYSQL_URL)

    @skipIf(not POSTGRESS_URL, 'mysql url undefined')
    def test_postgress(self):
        self._db_test(POSTGRESS_URL)

    def _db_test(self, db_url):
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

        db = Component.create(app)
        self.assertEqual(db.models, self.test_models)
        engine1 = db.engines['db1']
        engine2 = db.engines['db2']
        self.assertEqual(db.binds[models1.test_table1], engine1)
        self.assertEqual(db.binds[models2.test_table2], engine2)
        test_table1 = self.test_models['db1'].test_table1

        session = db()
        db.reset_all()
        Test = db.models['db1'].Test
        test = Test(id=5, title='test_title')
        session.add(test)
        session.commit()
        test = session.query(Test).filter_by(id=5).one()
        self.assertEqual(test.id, 5)
        self.assertEqual(test.title, 'test_title')

        test.title = 'test_title2'
        session.commit()
        cnt = session.query(Test).filter_by(id=5, title='test_title2').count()
        self.assertEqual(cnt, 1)

        session.delete(test)
        session.commit()
        cnt = session.query(Test).filter_by(id=5, title='test_title2').count()
        self.assertEqual(cnt, 0)

