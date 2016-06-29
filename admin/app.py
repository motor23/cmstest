import ikcms.apps.web
import ikcms.cli.app
import ikcms.cli.db


class App(ikcms.apps.web.App):

    def get_handler(self):
        from .handler import get_handler
        return get_handler(self)

    commands = {
        'admin': ikcms.cli.app.AppCli,
        'db': ikcms.cli.db.DBCli,
    }
