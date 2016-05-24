from ikcms.ws_components.base import WS_Component as WS_ComponentBase
from . import items


class WS_MenuComponent(WS_ComponentBase):
    name = 'menu'
    menu = {}

    def get_cfg(self, env):
        result = {}
        for id, items in self.menu.items():
            result[id] = [item.dict() for item in items]
        return result


ws_menu_component = WS_MenuComponent.create
