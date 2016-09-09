from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.query import Query

import ikcms.components.db.base


class SQLAComponent(ikcms.components.db.base.DBComponent):

    session_maker_class = sessionmaker
    query_class = Query

    def __init__(self, app, engines, models):
        super().__init__(app)
        self.engines = engines
        self.models = models
        self.binds = self.get_binds()
        self.session_maker = self.session_maker_class(
            binds=self.binds,
            query_cls=self.query_class,
        )

    @classmethod
    def create(cls, app):
        databases = getattr(app.cfg, 'DATABASES', {})
        database_params = getattr(app.cfg, 'DATABASE_PARAMS', {})
        engines = {}
        for db_id, url in databases.items():
            engines[db_id] = cls.create_engine(db_id, url, database_params)
        models = {db_id: cls.get_models(db_id) for db_id in databases}
        return cls(app, engines, models)

    @classmethod
    def create_engine(cls, db_id, url, engine_params):
        engine = create_engine(url, **engine_params)
        engine.db_id = db_id
        return engine

    def env_init(self, env):
        env.db = self()
        #env.models = self.env_models

    def env_close(self, env):
        env.db.close()

    @staticmethod
    def get_models(db_id):
        import models
        return getattr(models, db_id)

    def get_binds(self):
        binds = {}
        for db_id, engine in self.engines.items():
            for table in self.models[db_id].metadata.sorted_tables:
                binds[table] = engine
        return binds

    def __call__(self):
        return self.session_maker()

    def close(self):
        for engine in self.engines.values():
            engine.terminate()

    def create_all(self):
        for db_id, models in self.models.items():
            models.metadata.create_all(self.engines[db_id])

    def initial_all(self, session):
        from models.initial import initialize
        initialize(self.app, session)

    def drop_all(self):
        # XXX Need confirmation?
        for db_id, models in self.models.items():
            models.metadata.drop_all(self.engines[db_id])

    def reset_all(self):
        self.drop_all()
        self.create_all()


component = SQLAComponent.create_cls


