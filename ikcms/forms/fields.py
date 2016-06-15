from collections import OrderedDict
from .convs import ValidationError, RawValueTypeError

from . import convs
from . import validators
from . import widgets


__all__ = (
    'Field',
    'StringField',
    'IntField',
    'DictField',
    'ListField',
    'RawDictField',
    'RawlistField',
)


class Field:

    name = None
    label = None
    conv = convs.Converter
    fields = []
    validators = ()
    widget = widgets.Widget()

    raw_required = False
    to_python_default = None

    def __init__(self, context=None, parent=None):
        self.context = context and context.copy() or {}
        self.parent = parent
        self.fields = [f(context, self) for f in self.fields]
        self.named_fields = OrderedDict(
            [(f.name, f) for f in self.fields if f.name])
        self.conv = self.conv(self)
        self.validators = [v(self) for v in self.validators]

    def to_python(self, raw_value):
        value = self.conv.to_python(raw_value)
        for v in self.validators:
            value = v(value)
        return value

    def from_python(self, value):
        return self.conv.from_python(value)


class StringField(Field):
    conv = convs.Str
    validators = [
        validators.Required,
        validators.Regex,
        validators.Len,
    ]
    required = False
    regex = None
    min_len = None
    max_len = None


class IntField(Field):
    conv = convs.Int
    validators = [
        validators.Required,
        validators.Range,
    ]
    required = False
    min_value = None
    max_value = None


class DictField(Field):
    conv = convs.Dict
    validators = [
        validators.Required,
    ]
    required = False


class ListField(Field):
    conv = convs.List
    validators = [
        validators.Required,
        validators.Len,
    ]
    required = False
    min_len = None
    max_len = None


class RawDictField(Field):
    conv = convs.RawDict


class RawListField(Field):
    conv = convs.RawList
