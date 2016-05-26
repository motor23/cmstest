from hashlib import md5

import ikcms.ws_components.auth.base
from ikcms.ws_components.auth.base import user_required
from ikcms.ws_apps.base.messages import MessageForm
from ikcms.ws_apps.base import exc
from ikcms.forms import fields, validators


class mf_login(fields.StringField):
    name = 'login'
    label = 'Логин'
    validators = (validators.required,)

class mf_password(fields.StringField):
    name = 'password'
    label = 'Пароль'
    validators = (validators.required,)

class mf_key(fields.StringField):
    name = 'key'
    label = 'Ключ авторизации'
    validators = (validators.required,)


class WS_AuthComponent(ikcms.ws_components.auth.base.WS_AuthComponent):

    login_form = MessageForm([
        mf_login,
        mf_password,
    ])

    key_form = MessageForm([
        mf_login,
        mf_key,
    ])


    async def h_login(self, env, message):
        try:
            message = self.key_form.to_python(message)
            login = message['login']
            key = message['key']
            key = self.auth_by_key(env, login, key)
        except exc.MessageError:
            message = self.login_form.to_python(message)
            login = message['login']
            password = message['password']
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

    def auth_by_key(self, env, login, key):
        if key == key:
            return key
        else:
            return False


ws_auth_component = WS_AuthComponent.create
