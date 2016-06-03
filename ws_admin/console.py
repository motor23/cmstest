import sys
import json
import inspect
import asyncio
import websockets


class Console:

    def __init__(self, websocket, loop):
        self.websocket = websocket
        self.loop = loop
        self.commands = (
            ('send', self.send),
            ('login', self.login),
            ('logout', self.logout),
            ('cfg', self.cfg),
            ('list', self.list),
            ('get_item', self.get_item),
        )
        self.namespace = dict(self.commands)

    async def __call__(self):
        self.loop.add_reader(sys.stdin, self.read_command)
        print('===============================')
        print('Commands:')
        for key, value in self.commands:
            print("{}({})".format(
                key,
                ','.join(inspect.getargs(value.__code__)[0][1:])
            ))
        print('===============================')
        if len(sys.argv) > 1:
            self.login(sys.argv[1], sys.argv[1])

        while True:
            message = await self.websocket.recv()
            print('< {}'.format(message))

    def read_command(self):
        command = sys.stdin.readline()
        exec(command, self.namespace)

    def send(self, message):
        message['name'] = 'request'
        message['request_id'] = 'test'
        message = json.dumps(message)
        print('> {}'.format(message))
        asyncio.ensure_future(self.websocket.send(message))

    def login(self, login, password):
        self.send({'handler':'auth.login', 'body': {
                'login': login,
                'password': password,
            }
        })

    def logout(self):
        self.send({'handler':'auth.logout', 'body': {}})

    def cfg(self):
        self.send({'handler':'cinfo.cfg', 'body': {}})

    def list(self, stream, filters=None, order='+id', page=1, page_size=30):
        filters = filters or {}
        order = order or []
        self.send({
            'handler':'streams.action',
            'body': {
                'stream': stream,
                'action': 'list',
                'filters': filters,
                'order': order,
                'page': page,
                'page_size': page_size,
            },
        })

    def get_item(self, stream, item_id=None):
        self.send({
            'handler':'streams.action',
            'body': {
                'stream': stream,
                'action': 'get_item',
                'item_id': item_id,
            },
        })



async def console(loop):
    async with websockets.connect('ws://localhost:8888') as websocket:
        await Console(websocket, loop)()


loop = asyncio.get_event_loop()
loop.run_until_complete(console(loop))
