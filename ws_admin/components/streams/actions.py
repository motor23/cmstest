
class Base:
    name = None

    def __init__(self, stream):
        assert self.name is not None
        self.stream = stream

    async def handle(self, env): raise NotImplementedError

    def get_cfg(self, env):
        return {
            'name': self.name
        }



class List(Base):

    name = 'list'

    async def handle(self, env, message):
        items = await self.stream.get_form_items(
            env,
            self.stream.query(),
            self.stream.list_fields,
        )
        return {
            'stream': self.stream.name,
            'action': self.name,
            'items': items,
        }

