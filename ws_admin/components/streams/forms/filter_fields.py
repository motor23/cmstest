from ikcms.forms import fields


def simple_filter(op):
    def f(field, query, value):
        if value is not None:
            query = query.filter(field.name, op, value)
        return query
    return f


class ff_string(fields.StringField):
    filter = simple_filter('==')

class ff_int(fields.IntField):
    filter = simple_filter('==')

class ff_find(ff_string):
    filter = simple_filter('like')


class ff_id(ff_int):
    name = 'id'
    label = 'Id'

class ff_title(ff_find):
    name = 'title'
    label = 'Title'


