import os
import ikcms.apps.web

join = os.path.join

class Cfg(ikcms.apps.web.Cfg):
    SITE_ID = 'admin'

    HTTP_SERVER_HOST = 'localhost'
    HTTP_SERVER_PORT = 8000
    HTTP_SERVER_PIDFILE = property(
        lambda self: join(self.ROOT_DIR, 'run/admin_http.pid'))
    HTTP_SERVER_LOGFILE = property(
        lambda self: join(self.ROOT_DIR, 'log/admin_http.log'))

    WS_SERVER_HOST = 'localhost'
    WS_SERVER_PORT = 8888
    WS_SERVER_PIDFILE = property(
        lambda self: join(self.ROOT_DIR, 'run/admin_ws.pid'))
    WS_SERVER_LOGFILE = property(
        lambda self: join(self.ROOT_DIR, 'log/admin_ws.log'))

    DATABASES = {'main': 'mysql://root@localhost/web?charset=utf8'}

    LOG_LEVEL = 'DEBUG'
