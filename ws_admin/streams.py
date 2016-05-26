from ws_admin.components.streams import Stream
from ws_admin.components.streams.forms import (
    lf_id,
    lf_title,
    ff_id,
    ff_title,
    if_id,
    if_title,
)
from ws_admin.mappers import docs_mapper

streams = {}


class Docs(Stream):
    name = 'docs'
    title = 'Документы'
    mapper = docs_mapper
    list_fields = [
        lf_id,
        lf_title,
    ]
    filter_fields = [
        ff_id,
        ff_title,
    ]
    item_fields = [
        if_id,
        if_title,
    ]


Docs().register(streams)

