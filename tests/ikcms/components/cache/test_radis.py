from unittest import TestCase
from unittest.mock import MagicMock
from unittest import skipIf

from ikcms.utils.asynctests import asynctest
try:
    from ikcms.ws_components.cache.aioredis import component
    skip_test = False
except ImportError:
    skip_test = True

from tests.cfg import cfg

@skipIf(skip_test, 'Aioredis not installed')
class AIORedisTestCase(TestCase):

    @asynctest
    async def test_cache(self):
        app = self._create_app()

        cache = await component().create(app)

        await cache.delete(b'test_key')

        value = await cache.get(b'test_key')
        self.assertIsNone(value)

        await cache.set(b'test_key', b'test_value')
        value = await cache.get(b'test_key')
        self.assertEqual(value, b'test_value')

        await cache.delete(b'test_key')
        value = await cache.get(b'test_key')
        self.assertIsNone(value)

    def _create_app(self):
        app = MagicMock()
        del app.cache
        app.cfg = cfg
        return app
