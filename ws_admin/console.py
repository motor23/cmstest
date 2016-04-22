import asyncio
import websockets
import json
import sys
import inspect

message = {'name':'auth.login', 'body':{'login': 'motor', 'password': 'motor'}}

message = json.dumps(message)

class Console:

    def __init__(self, websocket, loop):
        self.websocket = websocket
        self.loop = loop
        self.namespace = {
            'send': self.send,
            'login': self.login,
            'logout': self.logout,
        }

    async def __call__(self):
        self.loop.add_reader(sys.stdin, self.read_command)
        print('===============================')
        print('Commands:')
        for key, value in self.namespace.items():
            print("{}({})".format(
                key,
                ','.join(inspect.getargs(value.__code__)[0][1:])),
            )
        print('===============================')
        while True:
            message = await self.websocket.recv()
            print('< {}'.format(message))

    def read_command(self):
        command = sys.stdin.readline()
        exec(command, self.namespace)

    def send(self, message):
        message = json.dumps(message)
        print('> {}'.format(message))
        asyncio.ensure_future(self.websocket.send(message))

    def login(self, login, password):
        self.send({'name':'auth.login', 'body': {
                'login': login,
                'password': password}})

    def logout(self):
        self.send({'name':'auth.loginout', 'body': {}})


async def console(loop):
    async with websockets.connect('ws://localhost:8888') as websocket:
         await Console(websocket, loop)()

loop = asyncio.get_event_loop()
loop.run_until_complete(console(loop))

