from iktomi.utils import cached_property
from ws_admin.components.streams import Stream
from ws_admin.components.streams.fields import (
    lf_id,
    lf_title,
    ff_id,
    ff_title,
)
from ws_admin.mappers import docs_mapper

streams = {}


class Docs(Stream):
    name = 'docs'
    mapper = docs_mapper
    list_fields = [
        lf_id,
        lf_title,
    ]
    filter_fields = [
        ff_id,
        ff_title,
    ]


Docs().register(streams)

