from ikcms.ws_apps.base.messages import MessageForm
from ikcms.forms import fields, validators, convs


class mf_item_id(fields.IntField):
    name = 'item_id'
    label = 'Идентификатор документа'
    to_python_default = None


class mf_filters(fields.RawDictField):
    name = 'filters'
    label = 'Словарь фильтров'
    to_python_default = {}


class mf_page(fields.IntField):
    name = 'page'
    label = 'Номер страницы'
    to_python_default = 1


class mf_page_size(fields.IntField):
    name = 'page_size'
    label = 'Размер страницы'
    to_python_default = 1


class OrderByConv(convs.Str):
    validators = (
        validators.required,
        validators.match(
            regex = '[+\-]{1}',
            message = 'Order value must startswith "+" or "-"',
        )
    )
    def to_python(self, field, value):
        values, errors = super().to_python(field, value)
        if values:
            return (values[0], values[1:]), errors


class mf_order(fields.StringField):
    name = 'order'
    label = 'Сортировка'
    conv = OrderByConv()
    to_python_default = ('+', 'id')

