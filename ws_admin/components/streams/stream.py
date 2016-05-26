from iktomi.utils import cached_property

from .forms import StreamForm
from . import actions
from . import exc


class StreamBase:
    name = None
    title = u'Название потока'
    actions = []

    def __init__(self):
        assert self.name is not None
        self.actions = [action(self) for action in self.actions]

    def register(self, registry):
        registry[self.name] = self

    def h_action(self, env, message):
        action_name = message.get('action')
        action = self.get_action(action_name)
        if action:
            return action.handle(env, message)
        else:
            raise exc.ActionNotFound(self, action_name)

    def get_action(self, name):
        for action in self.actions:
            if action.name == name:
                return action

    def get_cfg(self, env):
        return {
            'name': self.name,
            'title': self.title,
            'actions': list(map(lambda x: x.get_cfg(env), self.actions)),
        }



class Stream(StreamBase):
    mapper = None
    widget = 'Stream'
    max_limit = 100

    list_fields = []
    filter_fields = []
    default_order = ['+id']
    item_fields = []


    actions = [
        actions.List,
        actions.GetItem,
#        actions.create_draft,
#        actions.delete_draft,
#        actions.create_new_item,
#        actions.edit_item,
#        actions.get_field_block,
#        actions.set_field_value,
#        actions.delete_item,
    ]

    def get_list_form(self, env):
        return StreamForm(self.list_fields, self)

    def get_filter_form(self, env):
        return StreamForm(self.filter_fields, self)

    def get_order_form(self, env):
        return StreamForm(filter(lambda x: x.order, self.list_fields), self)

    def get_item_form(self, env, item={}):
        return StreamForm(self.item_fields, self)

    def query(self, keys=None):
        return self.mapper.select(keys)

    def get_cfg(self, env):
        list_form = self.get_list_form(env)
        filter_form = self.get_filter_form(env)
        return dict(
            super().get_cfg(env),
            widget=self.widget,
            max_limit=self.max_limit,
            list_fields=list_form.get_cfg(),
            filter_fields=filter_form.get_cfg(),
        )

