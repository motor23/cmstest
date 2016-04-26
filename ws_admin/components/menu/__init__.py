import ikcms.ws_components.base
from ikcms.ws_components.auth.base import user_required

from . import items

class WS_MenuComponent(ikcms.ws_components.base.WS_Component):

    name = 'menu'

    menu = {}

    def get_cfg(self, env):
        result = {}
        for id, items in self.menu.items():
            result[id] = list(map(lambda x: x.dict(), items))
        return result


ws_menu_component = WS_MenuComponent.create
