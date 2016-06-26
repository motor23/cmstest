import asyncio
from unittest import TestCase, skipIf
from unittest.mock import MagicMock
try:
    from ikcms.ws_components.cache.aiomcache import component
    skip_test = False
except ImportError:
    skip_test = True


@skipIf(skip_test, 'Aiomcache not installed')
class AIOMCacheTestCase(TestCase):

    def test_cache(self):
        app = MagicMock()
        del app.cache
        app.cfg.MEMCACHE_HOST = 'localhost'
        app.cfg.MEMCACHE_PORT = 11211

        async def run():
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

        asyncio.get_event_loop().run_until_complete(run())
