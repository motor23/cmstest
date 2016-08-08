from ikcms.orm import mappers

from models.main import metadata, Tag, Doc, User, User_Group, Group

registry = mappers.Registry({'main': metadata})

mappers.Base.from_model(registry, [Tag])
mappers.Base.from_model(registry, [Doc])
mappers.Base.from_model(registry, [User])
mappers.Base.from_model(registry, [Group])
mappers.Base.from_model(registry, [User_Group])
