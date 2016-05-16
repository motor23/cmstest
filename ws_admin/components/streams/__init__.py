import ikcms.ws_components.base
from . import exc
from .stream import Stream

__all__ = (
    'WS_Streams',
    'Stream',
)

class WS_Streams(ikcms.ws_components.base.WS_Component):
    
    name = 'streams'
    streams = {}

    def get_cfg(self, env):
        return {
            'streams': list(map(
                            lambda x: x.get_cfg(env), self.streams.values())),
        }

    async def h_action(self, env, message):
        stream_name = message.get('stream')
        if not stream_name:
            raise exc.FieldRequiredError('stream')
        stream = self.streams.get(stream_name)
        if stream:
            await stream.h_action(env, message)
        else:
            raise exc.StreamNotFound(stream_name)


    def handlers(self):
        return {
            'streams.action': self.h_action,
        }


ws_streams_component = WS_Streams.create
