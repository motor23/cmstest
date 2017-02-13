import ikcms.ws_components.base
from ikcms.ws_components.auth import restrict


class Component(ikcms.ws_components.base.Component):
    name = 'cinfo'

    @restrict()
    async def h_cfg(self, client, message):
        return {'cfg': self.cfg(client, names=message.get('components'))}

    @restrict()
    async def h_list(self, client, message):
        return {'list': self.list(client)}

    def cfg(self, client, names=None):
        if names is None:
            names = self.list(client)
        components = [self.app.get_component(name) for name in names]
        return self._get_components_cfg(client, components)

    def list(self, client):
        return self._get_components_names(self.app.components)

    def _get_components_names(self, components):
        return [x.name for x in components]

    def _get_components_cfg(self, client, components):
        return dict([
            (component.name, self._get_component_cfg(client, component))
            for component in components
        ])

    def _get_component_cfg(self, client, component):
        method = getattr(component, 'get_cfg', None)
        return method and method(client) or {}


cinfo = Component.create_cls
