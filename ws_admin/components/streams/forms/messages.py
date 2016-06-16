from ikcms.ws_apps.base.messages import MessageForm
from ikcms.forms import fields


class mf_item_id(fields.IntField):
    name = 'item_id'
    label = 'Идентификатор документа'
    raw_required = True
    required = True

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


class mf_order(fields.StringField):
    name = 'order'
    label = 'Сортировка'
    to_python_default = '+id'
    required = True
    regex = r'[+\-]{1}'
    regex_error = 'Order value must startswith "+" or "-"',


class mf_kwargs(fields.RawDictField):
    name = 'kwargs'
    label = 'Ключевые аргументы'
    to_python_default = {}


class mf_values(fields.RawDictField):
    name = 'values'
    label = 'Значения'
    raw_required = True
    required = True
