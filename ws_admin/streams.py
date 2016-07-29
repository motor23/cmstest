from ws_admin.components.streams import Stream
from ws_admin.components.streams.forms import list_fields
from ws_admin.components.streams.forms import filter_fields
from ws_admin.components.streams.forms import item_fields

from models.mappers import registry

streams = {}


class Docs(Stream):
    name = 'docs'
    title = 'Документы'
    mapper = registry['main']['Doc']
    list_fields = [
        list_fields.id,
        list_fields.title,
    ]
    filter_fields = [
        filter_fields.id,
        filter_fields.title,
    ]
    item_fields = [
        item_fields.id,
        item_fields.title,
    ]


Docs.register(streams)
