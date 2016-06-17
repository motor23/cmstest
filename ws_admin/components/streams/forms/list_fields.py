from ikcms.forms import fields


def simple_order(field, query, value):
    assert value in ['+', '-']
    return query.order_by(value + field.name)


class lf_str(fields.StringField):
    order = simple_order


class lf_int(fields.IntField):
    order = simple_order


class lf_id(lf_int):
    name = 'id'
    label = 'ID'


class lf_title(lf_str):
    name = 'title'
    label = 'Title'
