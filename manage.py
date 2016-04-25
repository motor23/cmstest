import os

from ikcms.cli import manage


ROOT = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    manage(['admin', 'ws_admin'], paths=[os.path.join(ROOT, 'third-party')])

