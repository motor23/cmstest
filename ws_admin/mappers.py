from ikcms import orm

from models.main import Tag, Doc


class MainMapper(orm.Mapper):
    db_id = 'main'


tags_mapper = orm.model_to_mapper(Tag, MainMapper)
docs_mapper = orm.model_to_mapper(Doc, MainMapper)
