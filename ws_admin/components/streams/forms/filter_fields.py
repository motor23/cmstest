from ikcms.forms import fields


__all__ = (
    'simple_filter',
    'String',
    'Int',
    'Find',
    'id',
    'title',
)


def simple_filter(op):
    def f(field, query, value):
        if value is not None:
            query = query.filter(field.name, op, value)
        return query
    return f



class String(fields.String):
    filter = simple_filter('==')


class Int(fields.Int):
    filter = simple_filter('==')


class Find(String):
    filter = simple_filter('like')



class id(Int):
    name = 'id'
    label = 'Id'


class title(Find):
    name = 'title'
    label = 'Title'


