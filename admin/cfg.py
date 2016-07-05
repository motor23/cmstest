import ikcms.apps.web


class Cfg(ikcms.apps.web.Cfg):
    SITE_ID = 'admin'

    HTTP_SERVER_HOST = 'localhost'
    HTTP_SERVER_PORT = 8000

    WS_SERVER_HOST = 'localhost'
    WS_SERVER_PORT = 8888

    DATABASES = {'main': 'mysql://root@localhost/web?charset=utf8'}

    LOG_LEVEL = 'DEBUG'
