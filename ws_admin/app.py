import ikcms.ws_apps.composite
import ikcms.ws_components.db
from . import components

from .menu import menu
from .streams import streams

class App(ikcms.ws_apps.composite.App):

    components = [
        ikcms.ws_components.db.sqla(),
        components.auth(),
        components.cinfo(),
        components.menu(menu=menu),
        components.streams(streams=streams),
    ]
