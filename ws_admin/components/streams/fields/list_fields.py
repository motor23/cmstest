from .base import ReadOnlyField

def simple_order(field, query, value):
    assert value in ['+', '-']
    return query.order_by(value + field.name)


class ListField(ReadOnlyField):
    widget = "ListField"
    order = simple_order


class LF_Id(ListField):
    name = 'id'
    label = 'ID'


class LF_Title(ListField):
    name = 'title'
    label = 'Title'


lf_id = LF_Id()
lf_title = LF_Title()
