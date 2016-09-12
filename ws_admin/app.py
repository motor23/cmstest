import ikcms.cli.ws_app
import ikcms.ws_apps.composite
import ikcms.ws_components.db
import ikcms.ws_components.cache.aioredis
import ikcms.ws_components.auth
import ikcms.ws_components.streams

from . import components

from .menu import menu
from . import streams

class App(ikcms.ws_apps.composite.App):

    components = [
        ikcms.ws_components.db.component(),
        ikcms.ws_components.cache.aioredis.component(),
        ikcms.ws_components.auth.component(),
        ikcms.ws_components.streams.component(streams=streams.registry),

        components.cinfo(),
        components.menu(menu=menu),
    ]

    commands = {
        'ws_admin': ikcms.cli.ws_app.WsAppCli,
    }
