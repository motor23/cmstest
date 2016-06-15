from functools import partial
from unittest import TestCase
from hypothesis import given
from hypothesis import strategies as s
from ikcms.forms.convs import *


class BoolConvTestCase(TestCase):
    def test_to_python(self):
        conv = Bool()
        to_python = partial(conv.to_python, None)

        self.assertEqual(None, to_python(None))
        self.assertEqual(False, to_python(False))
        self.assertEqual(False, to_python(''))
        self.assertEqual(False, to_python(0))
        self.assertEqual(True, to_python(True))
        self.assertEqual(True, to_python(object()))
        self.assertEqual(True, to_python(' '))
        self.assertEqual(True, to_python(1))

    def test_from_python(self):
        conv = Bool()
        from_python = partial(conv.from_python, None)

        self.assertEqual(None, from_python(None))
        self.assertEqual(False, from_python(False))
        self.assertEqual(False, from_python(''))
        self.assertEqual(False, from_python(0))
        self.assertEqual(True, from_python(True))
        self.assertEqual(True, from_python(object()))
        self.assertEqual(True, from_python(1))


class IntConvTestCase(TestCase):

    def test_to_python(self):
        conv = Int()
        to_python = partial(conv.to_python, None)

        self.assertEqual(None, to_python(None))
        self.assertEqual(1337, to_python(1337))
        self.assertEqual(1337, to_python('1337'))

    def test_from_python(self):
        conv = Int()
        from_python = partial(conv.from_python, None)

        self.assertEqual(None, from_python(None))
        self.assertEqual(1337, from_python(1337))


class StrConvTestCase(TestCase):
    def test_to_python(self):
        pass

    def test_from_python(self):
        pass


class ListConvTestCase(TestCase):
    def test_to_python(self):
        conv = List(conv=Int())
        to_python = partial(conv.to_python, None)

        self.assertEqual(None, to_python(None))
        self.assertEqual([], to_python([]))
        self.assertEqual([1], to_python([1]))
        self.assertEqual([1, 2], to_python([1, 2]))
        self.assertEqual([1], to_python(['1']))

        with self.assertRaises(RawValueTypeError) as ctx:
            to_python('not_a_list')

        with self.assertRaises(ValidationError) as ctx:
            to_python(['not_a_number'])

        self.assertEqual(ctx.exception.error, [Int.error_message])

    def test_from_python(self):
        conv = List(conv=Int())
        from_python = partial(conv.from_python, None)

        self.assertEqual(None, from_python(None))
