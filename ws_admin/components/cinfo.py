import ikcms.ws_components.base
from ikcms.ws_components.auth import restrict


class Component(ikcms.ws_components.base.Component):
    name = 'cinfo'

    @restrict()
    async def h_cfg(self, env, message):
        print('>>>>>>>>>>>>>>>>>>>', message)
        comp_names = self._get_components_names(self.app.components)
        names = message.get('components', comp_names)
        components = [self.app.get_component(name) for name in names]
        cfg = self._get_components_cfg(env, components)
        return {'cfg': cfg}

    @restrict()
    async def h_list(self, env, message):
        comp_names = self._get_components_names(self.app.components)
        return {'list': comp_names}

    def _get_components_names(self, components):
        return [x.name for x in components]

    def _get_components_cfg(self, env, components):
        return dict([
            (component.name, self._get_component_cfg(env, component))
            for component in components
        ])

    def _get_component_cfg(self, env, component):
        method = getattr(component, 'get_cfg', None)
        return method and method(env) or {}


cinfo = Component.create_cls
