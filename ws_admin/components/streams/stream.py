from collections import OrderedDict

from iktomi.utils import cached_property
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
            raise exc.ActionNotFound(self.stream, action_name)

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
    limits = [30, 50, 100]

    list_fields = []
    filter_fields = []
    default_order = ['+id']
    item_fields = []


    actions = [
        actions.List,
#        actions.create_draft,
#        actions.delete_draft,
#        actions.create_new_item,
#        actions.edit_item,
#        actions.get_field_block,
#        actions.set_field_value,
#        actions.delete_item,
    ]

    def __init__(self):
        super().__init__()
        self.list_fields_dict = OrderedDict(
                                    [(x.name, x) for x in self.list_fields])
        self.order_fields_dict = OrderedDict(
                            [(x.name, x) for x in self.list_fields if x.order])
        self.filter_fields_dict = OrderedDict(
                                    [(x.name, x) for x in self.filter_fields])
        self.item_fields_dict = OrderedDict(
                                    [(x.name, x) for x in self.item_fields])

    def query(self, keys=None):
        return self.mapper.select(keys)

    def get_cfg(self, env):
        return dict(
            super().get_cfg(env),
            widget = self.widget,
            limits = self.limits,
            list_fields = list(map(lambda x: x.get_cfg(env), self.list_fields)),
            filter_fields = list(map(
                                lambda x: x.get_cfg(env), self.filter_fields)),
        )

    def fields_from_python(self, env, items, fields_dict):
        raw_items = []
        for item in items:
            raw_item = {'id': item['id']}
            for field in fields_dict.values():
                raw_item.update(field.from_python(env, self, item))
            raw_items.append(raw_item)
        return raw_items

    def fields_accept(self, env, raw_item, fields_dict):
        errors = {}
        values = {}
        for name in raw_item.keys():
            field = fields_dict.get(name)
            if not field:
                raise FieldNotFound(self, name)
            value, errors = field.accept(env, self, raw_item)
            if value:
                values.update(value)
            else:
                errors.update(error)
        return values, errors

