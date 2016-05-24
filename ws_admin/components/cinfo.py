from ikcms.ws_components.base import WS_Component as WS_ComponentBase
from ikcms.ws_components.auth.base import user_required


class WS_CInfoComponent(WS_ComponentBase):
    name = 'cinfo'

    @user_required
    async def h_cfg(self, env, message):
        comp_names = self._get_components_names(self.app.components)
        names = message.get('components', comp_names)
        components = [self.app.get_component(name) for name in names]
        cfg = self._get_components_cfg(env, components)
        return {'cfg': cfg}

    @user_required
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

    def handlers(self):
        return {
            'cinfo.cfg.request': self.h_cfg,
            'cinfo.list.request': self.h_list,
        }

ws_cinfo_component = WS_CInfoComponent.create
