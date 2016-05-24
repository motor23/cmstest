from ikcms.ws_components.base import WS_Component as WS_ComponentBase
from .exc import FieldRequiredError
from .exc import StreamNotFound
from .stream import Stream

__all__ = (
    'WS_Streams',
    'Stream',
)


class WS_Streams(WS_ComponentBase):
    name = 'streams'
    streams = {}

    def get_cfg(self, env):
        return {
            'streams': [s.get_cfg(env) for s in self.streams.values()],
        }

    async def h_action(self, env, message):
        stream_name = message.get('stream')
        if not stream_name:
            raise FieldRequiredError('stream')
        stream = self.streams.get(stream_name)
        if stream:
            return await stream.h_action(env, message)
        else:
            raise StreamNotFound(stream_name)

    def handlers(self):
        return {
            'streams.action.request': self.h_action,
        }


ws_streams_component = WS_Streams.create
