from collections import OrderedDict
from .actions import List
from .exc import ActionNotFound
from .exc import FieldNotFoundError


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
            raise ActionNotFound(self.name, action_name)

    def get_action(self, name):
        for action in self.actions:
            if action.name == name:
                return action

    def get_cfg(self, env):
        return {
            'name': self.name,
            'title': self.title,
            'actions': [action.get_cfg(env) for action in  self.actions],
        }


class Stream(StreamBase):
    mapper = None
    widget = 'Stream'
    limits = [10, 20, 30, 50, 100]

    list_fields = []
    filter_fields = []
    default_order = ['+id']
    item_fields = []

    actions = [
        List,
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
            widget=self.widget,
            limits=self.limits,
            list_fields=[field.get_cfg(env) for field in  self.list_fields],
            filter_fields=[field.get_cfg(env) for field in self.filter_fields],
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
                # XXX: no such exception
                raise FieldNotFoundError(self, name)
            value, errors = field.accept(env, self, raw_item)
            if value:
                values.update(value)
            else:
                # XXX: unbound local variable `error`
                errors.update(error)
        return values, errors

