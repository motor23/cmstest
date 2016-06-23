from ikcms.ws_apps.base.exc import MessageError


__all__ = (
    'AuthError',
    'AuthLoginError',
    'AuthKeyError',
)


class AuthError(MessageError):
    pass


class AuthLoginError(AuthError):
    message = 'Incorrect login or password'


class AuthKeyError(AuthError):
    message = 'Incorrect auth key'

