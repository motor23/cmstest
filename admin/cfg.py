import ikcms.apps.web


class Cfg(ikcms.apps.web.Cfg):

    SITE_ID = 'admin'
    WS_SERVER_URL = 'ws://localhost:8888/ws'

    DATABASES = {'': 'mysql://root@localhost/web?charset=utf8'}
#    DATABASES = {'': 'aiopg://root@localhost/web?charset=utf8'}
    LOG_LEVEL = 'DEBUG'
