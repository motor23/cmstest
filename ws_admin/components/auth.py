from hashlib import md5

import ikcms.ws_components.auth.base
from ikcms.ws_components.auth.base import user_required
user_required
from ikcms.ws_apps.base.exc import FieldRequiredError


class WS_AuthComponent(ikcms.ws_components.auth.base.WS_AuthComponent):

    async def h_login(self, env, message):
        login = message.get('login')
        if not login:
            raise FieldRequiredError('login')
        password = message.get('password')
        key = message.get('key')
        if password:
            key = self.auth_by_password(env, login, password)
        elif key:
            key = self.auth_by_key(env, login, key)
        else:
            raise FieldRequiredError(('password', 'key'))
        if key:
            env.user = {'login': login}
            await env.send('auth.login_ok', {
                'login': login,
                'key': key,
                'session_id': env.session_id,
            })
        else:
            await env.send('auth.login_error',
                {'reason': 'Wrong login or password'})

    @user_required
    async def h_logout(self, env, message):
        env.user = None
        await env.send('auth.logout_ok', {})

    def auth_by_password(self, env, login, password):
        key = md5(login.encode('utf8')).hexdigest()
        if login==password:
            return key
        else:
            return False

    def auth_by_key(self, env, login, key):
        key = md5(login.encode('utf8')).hexdigest()
        if login==password:
            return key
        else:
            return False


ws_auth_component = WS_AuthComponent.create
