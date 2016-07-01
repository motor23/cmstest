from ikcms.forms import fields


__all__ = (
    'simple_order',
    'String',
    'Int',
    'id',
    'title',
)


def simple_order(field, query, value):
    assert value in ['+', '-']
    field = self.context['stream'].mapper.table.c[field.name]
    if value == '+':
        return query.order_by(field.name)
    else:
        return query.order_by(field.name.desc())


class String(fields.String):
    order = simple_order


class Int(fields.Int):
    order = simple_order


class id(Int):
    name = 'id'
    label = 'ID'


class title(String):
    name = 'title'
    label = 'Title'
