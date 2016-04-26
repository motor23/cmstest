import ikcms.ws_apps.composite
from .components.auth import ws_auth_component
from .components.cinfo import ws_cinfo_component
from .components.menu import ws_menu_component

from .menu import menu

class App(ikcms.ws_apps.composite.App):

    components = [
        ws_auth_component(),
        ws_cinfo_component(),
        ws_menu_component(menu=menu),
    ]

