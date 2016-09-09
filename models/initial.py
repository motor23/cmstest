import asyncio

from .mappers import registry
#from models.main import User
import ws_admin


def initialize(app, session):
    ws_app = ws_admin.App(app.cfg)
    async def awrapper():
        session = await ws_app.db()
        for mapper in registry.create_schema_mappers:
            await mapper.schema_initialize(session)
        await session.commit()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(awrapper())

