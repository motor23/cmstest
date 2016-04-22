from ikcms.cli.app import AppCli
from ikcms.cli.db import DBCli
from .app import App
from .cfg import Cfg

cli_commands = {
    'admin': AppCli(App, Cfg),
    'db': DBCli(App, Cfg),
}
