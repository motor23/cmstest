import asyncio
from unittest import TestCase
from unittest.mock import MagicMock
from ikcms.ws_components.cache.aioredis import Cache

class AIORedisTestCase(TestCase):

    def test_cache(self):
        app = MagicMock()
        app.cfg.REDIS_HOST = 'localhost'
        app.cfg.REDIS_PORT = 6379

        @asyncio.coroutine
        def run():
            cache = yield from Cache.create(app)

            yield from cache.delete(b'test_key')

            value = yield from cache.get(b'test_key')
            self.assertIsNone(value)

            yield from cache.set(b'test_key', b'test_value')
            value = yield from cache.get(b'test_key')
            self.assertEqual(value, b'test_value')

            yield from cache.delete(b'test_key')
            value = yield from cache.get(b'test_key')
            self.assertIsNone(value)

        asyncio.get_event_loop().run_until_complete(run())
