from ikcms.orm import Mapper
from ikcms.orm import model_to_mapper

from models.main import Tag, Doc, User, User_Group, Group


class MainMapper(Mapper):
    db_id = 'main'




tags_mapper_front = model_to_mapper(Tag, Mapper, db_id='front')
tags_mapper_admin = model_to_mapper(Tag, Mapper, db_id='admin')

docs_mapper = model_to_mapper(Doc, MainMapper)
user_mapper = model_to_mapper(User, MainMapper)
group_mapper = model_to_mapper(Group, MainMapper)
user_group_mapper = model_to_mapper(User_Group, MainMapper)
