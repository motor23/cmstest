from hashlib import md5
import ikcms.ws_components.auth.base
from ikcms.ws_components.auth.base import user_required
from ikcms.ws_apps.base.forms import MessageForm

from . import exc
from .forms import message_fields

__all__ = (
    'Auth',
    'auth',
)

class Auth(ikcms.ws_components.auth.base.Component):

    class LoginForm(MessageForm):
        fields = [
            message_fields.login,
            message_fields.password,
        ]

    class KeyForm(MessageForm):
        fields = [
            message_fields.key,
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
            raise exc.AuthLoginError

    def auth_by_key(self, env, key):
        try:
            login, password = key.split('.')
        except ValueError:
            raise exc.AuthKeyError


auth = Auth.create_cls
