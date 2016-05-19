from iktomi.forms.convs import ValidationError

from . import convs


class ReadOnlyField:

    name = None
    label = 'Field label'
    conv_class = convs.Char
    widget = None

    def __init__(self):
        assert self.name is not None
        assert self.widget is not None
        self.conv = self.create_conv()

    def create_conv(self):
        return self.conv_class(self)

    def from_python(self, env, stream, item):
        return {self.name: self.conv.from_python(item[self.name])}

    def get_cfg(self, env):
        return {
            'name': self.name,
            'label': self.label,
            'widget': self.widget,
        }


class Field(ReadOnlyField):

    validators = ()

    def accept(self, env, stream, item):
        try:
            value = self.conv.to_python(item[self.name])
            for v in self.validators:
                value = v(self, value)
        except ValidationError as e:
            return {}, {self.name: e.message}
        return {self.name: value}, {}

