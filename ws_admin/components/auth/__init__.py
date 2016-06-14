from hashlib import md5
from ikcms.ws_components.auth.base import WS_AuthComponent as WS_AuthComponentBase
from ikcms.ws_components.auth.base import user_required
from ikcms.ws_apps.base.messages import MessageForm
from ikcms.ws_apps.base import exc
from ikcms.forms import fields, validators


class mf_login(fields.StringField):
    name = 'login'
    label = 'Логин'
    raw_required = True
    required = True


class mf_password(fields.StringField):
    name = 'password'
    label = 'Пароль'
    raw_required = True
    required = True


class mf_key(fields.StringField):
    name = 'key'
    label = 'Ключ авторизации'
    raw_required = True
    required = True


class AuthError(exc.MessageError): pass


class AuthLoginError(AuthError):
    message = 'Incorrect login or password'


class AuthKeyError(AuthError):
    message = 'Incorrect auth key'


class WS_AuthComponent(WS_AuthComponentBase):

    class LoginForm(MessageForm):
        fields = [
            mf_login,
            mf_password,
        ]

    class KeyForm(MessageForm):
        fields = [
            mf_key,
        ]

    async def h_login(self, env, message):
        try:
            message = self.KeyForm().to_python(message)
            key, login = self.auth_by_key(env, message['key'])
        except exc.MessageError:
            message = self.LoginForm().to_python(message)
            key, login = self.auth_by_password(
                                    env, message['login'], message['password'])
        env.user = {'login': login}
        return {
            'login': login,
            'key': key,
            'session_id': env.session_id,
        }

    @user_required
    async def h_logout(self, env, message):
        env.user = None
        return {}

    def auth_by_password(self, env, login, password):
        key = md5(login.encode('utf8')).hexdigest()
        if login == password:
            return login, key
        else:
            raise AuthLoginError

    def auth_by_key(self, env, key):
        try:
            login, password = key.split('.')
        except ValueError:
            raise AuthKeyError


ws_auth_component = WS_AuthComponent.create
