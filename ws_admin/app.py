import ikcms.ws_apps.composite
from ikcms.ws_components.db.sqla import ws_sqla_component

from .components.auth import ws_auth_component
from .components.cinfo import ws_cinfo_component
from .components.menu import ws_menu_component
from .components.streams import ws_streams_component

from .menu import menu
from .streams import streams

class App(ikcms.ws_apps.composite.App):

    components = [
        ws_sqla_component(),
        ws_auth_component(),
        ws_cinfo_component(),
        ws_menu_component(menu=menu),
        ws_streams_component(streams=streams),
    ]
