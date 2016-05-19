from hashlib import md5

import ikcms.ws_components.auth.base
from ikcms.ws_components.auth.base import user_required
from ikcms.ws_apps.composite.exc import FieldRequiredError


class WS_AuthComponent(ikcms.ws_components.auth.base.WS_AuthComponent):

    async def h_login(self, env, message):
        key = message.get('key')
        login = message.get('login')
        password = message.get('password')
        if key:
            key = self.auth_by_key(env, key)
        else:
            if not login:
                raise FieldRequiredError('login')
            if not password:
                raise FieldRequiredError('password')
            key = self.auth_by_password(env, login, password)
        if key:
            env.user = {'login': login}
            return {
                'status': 'ok',
                'login': login,
                'key': key,
                'session_id': env.session_id,
            }
        else:
            return {
                'status': 'failed',
                'reason': 'Wrong login or password',
            }

    @user_required
    async def h_logout(self, env, message):
        env.user = None
        return {'status': 'ok'}

    def auth_by_password(self, env, login, password):
        key = md5(login.encode('utf8')).hexdigest()
        if login==password:
            return key
        else:
            return False

    def auth_by_key(self, env, key):
        if key == key:
            return key
        else:
            return False


ws_auth_component = WS_AuthComponent.create
