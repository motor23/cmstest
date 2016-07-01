from ikcms.forms import fields


__all__ = (
    'simple_filter',
    'String',
    'Int',
    'Find',
    'id',
    'title',
)


def eq_filter(field, query, value):
    column = field.context['stream'].mapper.table.c[field.name]
    if value is not None:
        query = query.where(column==value)
    return query

def like_filter(field, query, value):
    column = field.context['stream'].mapper.table.c[field.name]
    if value is not None:
        query = query.where(column.like("%{}%".format(value)))
    return query


class String(fields.String):
    filter = eq_filter

class Int(fields.Int):
    filter = eq_filter

class Find(String):
    filter = like_filter



class id(Int):
    name = 'id'
    label = 'Id'


class title(Find):
    name = 'title'
    label = 'Title'


