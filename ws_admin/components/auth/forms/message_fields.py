from ikcms.forms import fields


__all__ = (
    'login',
    'password',
    'key',
)


class login(fields.String):
    name = 'login'
    label = 'Логин'
    raw_required = True
    required = True


class password(fields.String):
    name = 'password'
    label = 'Пароль'
    raw_required = True
    required = True


class key(fields.String):
    name = 'key'
    label = 'Ключ авторизации'
    raw_required = True
    required = True


