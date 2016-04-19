from ikcms.cli.ws_app import WsAppCli

from admin import Cfg

from .app import App

cli_commands = {
    'ws_admin': WsAppCli(App, Cfg),
}
