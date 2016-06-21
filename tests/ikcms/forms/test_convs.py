from datetime import date
from unittest import TestCase
from unittest.mock import MagicMock
from ikcms.forms.convs import *
from ikcms.forms import exc
from ikcms.forms import fields


class BoolConvTestCase(TestCase):
    def test_to_python(self):
        field = MagicMock()
        conv = Bool(field)
        self.assertEqual(None, conv.to_python(None))
        self.assertEqual(False, conv.to_python(False))
        self.assertEqual(True, conv.to_python(True))
        with self.assertRaises(exc.RawValueTypeError):
            conv.to_python('')

    def test_from_python(self):
        field = MagicMock()
        conv = Bool(field)
        self.assertEqual(None, conv.from_python(None))
        self.assertEqual(False, conv.from_python(False))
        self.assertEqual(True, conv.from_python(True))


class IntConvTestCase(TestCase):
    def test_to_python(self):
        field = MagicMock()
        conv = Int(field)
        self.assertEqual(None, conv.to_python(None))
        self.assertEqual(1, conv.to_python(1))
        with self.assertRaises(exc.RawValueTypeError):
            conv.to_python('1')

    def test_from_python(self):
        field = MagicMock()
        conv = Int(field)
        self.assertEqual(None, conv.from_python(None))
        self.assertEqual(1, conv.from_python(1))


class StrConvTestCase(TestCase):
    def test_to_python(self):
        field = MagicMock()
        conv = Str(field)
        self.assertEqual(None, conv.to_python(None))
        self.assertEqual('str', conv.to_python('str'))
        with self.assertRaises(exc.RawValueTypeError):
            conv.to_python(True)

    def test_from_python(self):
        field = MagicMock()
        conv = Str(field)
        self.assertEqual(None, conv.from_python(None))
        self.assertEqual('str', conv.from_python('str'))


class ListConvTestCase(TestCase):
    def test_to_python(self):
        field = fields.Field()
        field.conv = Int(field)
        conv = List(field)
        self.assertEqual(None, conv.to_python(None))
        self.assertEqual([], conv.to_python([]))
        self.assertEqual([1], conv.to_python([1]))
        self.assertEqual([1, 2], conv.to_python([1, 2]))
        with self.assertRaises(exc.RawValueTypeError):
            conv.to_python('invalid')
        with self.assertRaises(exc.RawValueTypeError):
            conv.to_python(['invalid'])

    def test_from_python(self):
        field = MagicMock()
        field.name = 'TestField'
        field.conv = Int(field)
        field.from_python = field.conv.from_python
        conv = List(field)
        self.assertEqual(None, conv.from_python(None))
        self.assertEqual([], conv.from_python([]))
        self.assertEqual([1, 2], conv.from_python([1, 2]))


class DictConvTestCase(TestCase):
    def test_to_python(self):
        str_field = fields.Field()
        str_field.name = 'str_field'
        str_field.conv = Str(str_field)
        str_field.raw_required = False
        str_field.to_python_default = MagicMock()
        int_field = fields.Field()
        int_field.name = 'int_field'
        int_field.conv = Int(int_field)
        int_field.raw_required = False
        int_field.to_python_default = MagicMock()
        int_field.to_python = int_field.to_python
        field = fields.Field()
        field.fields = [str_field, int_field]
        conv = Dict(field)
        default_raw = {
        }
        default_result = {
            'str_field': str_field.to_python_default,
            'int_field': int_field.to_python_default,
        }
        first_raw = {
            'str_field': 'str',
            'int_field': 1,
        }
        first_result = {
            'str_field': 'str',
            'int_field': 1,
        }
        self.assertEqual(None, conv.to_python(None))
        self.assertEqual(default_result, conv.to_python(default_raw))
        self.assertEqual(first_result, conv.to_python(first_raw))

    def test_from_python(self):
        field = MagicMock()
        str_field = MagicMock()
        str_field.name = 'str_field'
        str_field.conv = Str(str_field)
        str_field.raw_required = False
        str_field.from_python = str_field.conv.from_python
        int_field = MagicMock()
        int_field.name = 'int_field'
        int_field.conv = Int(int_field)
        int_field.raw_required = False
        int_field.from_python = int_field.conv.from_python
        field = MagicMock()
        field.named_fields = {'str_field': str_field, 'int_field': int_field}
        conv = Dict(field)

        self.assertEqual(None, conv.from_python(None))
        self.assertEqual({}, conv.from_python({}))


class DateConvTestCase(TestCase):
    def test_to_python(self):
        field = MagicMock()
        field.format = '%Y-%m-%d'
        conv = Date(field)
        self.assertEqual(None, conv.to_python(None))
        self.assertEqual(date(2016, 6, 15), conv.to_python('2016-06-15'))
        with self.assertRaises(exc.ValidationError) as e:
            conv.to_python('invalid')
        self.assertEqual(e.exception.error, Date.error_not_valid)

    def test_from_python(self):
        field = MagicMock()
        field.format = '%Y-%m-%d'
        conv = Date(field)
        self.assertEqual(None, conv.from_python(None))
        self.assertEqual('2016-06-15', conv.from_python(date(2016, 6, 15)))
