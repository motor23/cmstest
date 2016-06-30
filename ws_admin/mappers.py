from ikcms.orm import Mapper
from ikcms.orm import model_to_mapper

from models.main import Tag, Doc


class MainMapper(Mapper):
    db_id = 'main'


tags_mapper = model_to_mapper(Tag, MainMapper)
docs_mapper = model_to_mapper(Doc, MainMapper)
