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
            ('new_item', self.new_item),
            ('create_item', self.create_item),
            ('update_item', self.update_item),
            ('delete_item', self.delete_item),
        )
        self.namespace = dict(self.commands)

    async def __call__(self):
        self.loop.add_reader(sys.stdin, self.read_command)
        print('===============================')
        print('Commands:')
        for key, value in self.commands:
            print("{}{}".format(
                key,
                str(inspect.signature(value))
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
        }})

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

    def new_item(self, stream, kwargs=None):
        self.send({
            'handler':'streams.action',
            'body': {
                'stream': stream,
                'action': 'new_item',
                'kwargs': kwargs or {},
            },
        })

    def create_item(self, stream, values, kwargs=None):
        self.send({
            'handler':'streams.action',
            'body': {
                'stream': stream,
                'action': 'create_item',
                'values': values,
                'kwargs': kwargs or {},
            },
        })

    def update_item(self, stream, item_id, values):
        self.send({
            'handler':'streams.action',
            'body': {
                'stream': stream,
                'action': 'update_item',
                'item_id': item_id,
                'values': values,
            },
        })

    def delete_item(self, stream, item_id):
        self.send({
            'handler':'streams.action',
            'body': {
                'stream': stream,
                'action': 'delete_item',
                'item_id': item_id,
            },
        })


async def console(loop):
    async with websockets.connect('ws://localhost:8888') as websocket:
        await Console(websocket, loop)()


loop = asyncio.get_event_loop()
loop.run_until_complete(console(loop))
