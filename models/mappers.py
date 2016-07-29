from ikcms.orm import mappers

from models.main import metadata, Tag, Doc, User, User_Group, Group

registry = mappers.Registry({'main': metadata})

mappers.Base.from_model(registry, 'Tag', [Tag])
mappers.Base.from_model(registry, 'Doc', [Doc])
mappers.Base.from_model(registry, 'User', [User])
mappers.Base.from_model(registry, 'Group', [Group])
mappers.Base.from_model(registry, 'UserGroup', [User_Group])
