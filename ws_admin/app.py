import ikcms.ws_apps.base

class App(ikcms.ws_apps.base.App):

    def get_handlers(self):
        from .handlers import handlers
        return handlers

