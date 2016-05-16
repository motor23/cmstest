from iktomi.utils import cached_property
from ws_admin.components.streams import Stream
from ws_admin.components.streams.list_fields import lf_id, lf_title
from ws_admin.mappers import docs_mapper

streams = {}


class Docs(Stream):
    name = 'docs'
    mapper = docs_mapper
    list_fields = [
        lf_id,
        lf_title,
    ]


Docs().register(streams)

