import ikcms.cli.ws_app
import ikcms.ws_apps.composite
import ikcms.ws_components.db.sqla
import ikcms.ws_components.cache.aioredis
import ikcms.ws_components.auth.base

from . import components

from .menu import menu
from .streams import streams

class App(ikcms.ws_apps.composite.App):

    components = [
        ikcms.ws_components.db.sqla.component(),
        ikcms.ws_components.cache.aioredis.component(),
        ikcms.ws_components.auth.base.component(),

        components.cinfo(),
        components.menu(menu=menu),
        components.streams(streams=streams),
    ]

    commands = {
        'ws_admin': ikcms.cli.ws_app.WsAppCli,
    }
