from .base import Field
from . import convs


def simple_filter(op):
    def f(field, query, value):
        if value is not None:
            query = query.filter(field.name, op, value)
        return query
    return f


class FilterField(Field):
    filter = simple_filter('==')


class FF_String(FilterField):
    widget = "FilterStringWidget"


class FF_Int(FF_String):
    conv_class = convs.Int


class FF_Find(FF_String):
    filter = simple_filter('like')


class FF_Id(FF_Int):
    name = 'id'
    label = 'Id'


class FF_Title(FF_Find):
    name = 'title'
    label = 'Title'


ff_id = FF_Id()
ff_title = FF_Title()
