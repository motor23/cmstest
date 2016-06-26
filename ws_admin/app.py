import ikcms.ws_apps.composite
import ikcms.ws_components.db.sqla
import ikcms.ws_components.cache.aioredis

from . import components

from .menu import menu
from .streams import streams

class App(ikcms.ws_apps.composite.App):

    components = [
        ikcms.ws_components.db.sqla.component(),
        ikcms.ws_components.cache.aioredis.component(),

        components.auth(),
        components.cinfo(),
        components.menu(menu=menu),
        components.streams(streams=streams),
    ]
