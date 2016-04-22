import ikcms.ws_apps.composite
from .components.auth import ws_auth_component

class App(ikcms.ws_apps.composite.App):

    components = [
        ws_auth_component(),
    ]

