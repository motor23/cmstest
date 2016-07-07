from ikcms.orm import Mapper
from ikcms.orm import model_to_mapper

from models.main import Tag, Doc, User, User_Group, Group


tags_mapper = model_to_mapper(Tag, Mapper, db_id='main')
docs_mapper = model_to_mapper(Doc, Mapper, db_id='main')
users_mapper = model_to_mapper(User, Mapper, db_id='main')
group_mapper = model_to_mapper(Group, Mapper, db_id='main')
user_group_mapper = model_to_mapper(User_Group, Mapper, db_id='main')
