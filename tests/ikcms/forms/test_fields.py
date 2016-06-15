from unittest import TestCase
from ikcms.forms.fields import BaseField
from ikcms.forms.convs import RawValueTypeError
from ikcms.forms.convs import NOTSET


class FieldTestCase(TestCase):
    pass

    # def test_to_python_default(self):
    #     field = BaseField(form=None, name='test')
    #     self.assertEqual(field.to_python(NOTSET), NOTSET)
