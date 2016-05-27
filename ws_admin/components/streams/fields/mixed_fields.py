from .base import Field
from . import convs
from .list_fields import simple_order
from .filter_fields import simple_filter


class MixedField(Field):

    order = simple_order
    filter = simple_filter('==')


class XF_String(MixedField):
    widget = "StringField"


class XF_Int(XF_String):
    conv_class = convs.Int


class XF_Id(FF_Int):
    widget = "IdField"
    name = 'id'
    label = 'Id'


class XF_Title(XF_Title):
    name = 'title'
    label = 'Title'
    filter = simple_filter('like')


xf_id = XF_Id()
xf_title = XF_Title()
