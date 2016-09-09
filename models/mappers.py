from ikcms.orm import mappers

from ikcms.ws_components import auth

from models.main import metadata, Tag, Doc

registry = mappers.Registry({'main': metadata})

auth.mappers.AdminGroup.create(registry, db_id='main')
auth.mappers.AdminUser.create(registry, db_id='main')

mappers.Base.from_model(registry, [Tag])
mappers.Base.from_model(registry, [Doc])

registry.create_schema()

