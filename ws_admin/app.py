import ikcms.ws_apps.composite

class App(ikcms.ws_apps.composite.App):

    def get_handlers(self):
        from .handlers import handlers
        return handlers

