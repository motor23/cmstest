from ikcms.cli.app import AppCli
from .app import App
from .cfg import Cfg

cli_commands = {
    'admin': AppCli(App, Cfg),
}
