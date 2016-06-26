import ikcms.ws_components.base


class Component(ikcms.ws_components.base.Component):
    name = 'menu'
    menu = {}

    def get_cfg(self, env):
        result = {}
        for id, items in self.menu.items():
            result[id] = [item.dict() for item in items]
        return result


menu = Component.create_cls
