import ikcms.apps.web

class App(ikcms.apps.web.App):

    def get_handler(self):
        from .handler import get_handler
        return get_handler(self)

