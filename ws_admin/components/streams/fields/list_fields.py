from .base import ReadOnlyField


class ListField(ReadOnlyField):
    widget = "ListField"


class LF_Id(ListField):
    name = 'id'
    label = 'ID'


class LF_Title(ListField):
    name = 'title'
    label = 'Title'


lf_id = LF_Id()
lf_title = LF_Title()
