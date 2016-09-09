from unittest import TestCase, skipIf
from unittest.mock import MagicMock
try:
    from ikcms.components.cache.memcache import component
    skip_test = False
except ImportError:
    skip_test = True

from tests.cfg import cfg


@skipIf(skip_test, 'Memcache not installed')
class MemcacheTestCase(TestCase):

    def test_cache(self):
        app = self._create_app()

        cache = component().create(app)
        cache.delete(b'test_key')

        value = cache.get(b'test_key')
        self.assertIsNone(value)

        cache.set(b'test_key', 'test_value')
        value = cache.get(b'test_key')
        self.assertEqual(value, 'test_value')

        cache.delete(b'test_key')
        value = cache.get(b'test_key')
        self.assertIsNone(value)

        app = self._create_app()

        cache_with_key = component(prefix=b'test_prefix-').create(app)
        cache.delete(b'test_prefix-test_key')
        cache_with_key.set(b'test_key', 'test_value')

        value = cache.get(b'test_prefix-test_key')
        self.assertEqual(value, 'test_value')
        value = cache_with_key.get(b'test_key')
        self.assertEqual(value, 'test_value')
        cache_with_key.delete(b'test_key')
        value = cache.get(b'test_prefix-test_key')
        self.assertIsNone(value)

    def _create_app(self):
        app = MagicMock()
        del app.cache
        app.cfg = cfg
        return app
