import asyncio
from unittest import TestCase
from unittest.mock import MagicMock
from ikcms.ws_components.cache.aioredis import component

class AIORedisTestCase(TestCase):

    def test_cache(self):
        app = MagicMock()
        del app.cache
        app.cfg.REDIS_HOST = 'localhost'
        app.cfg.REDIS_PORT = 6379

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
