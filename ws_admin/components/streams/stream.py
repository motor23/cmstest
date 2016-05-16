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
    order_fields = []
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

    def query(self, keys=None):
        return self.mapper.select(keys)

    def get_cfg(self, env):
        return dict(
            super().get_cfg(env),
            widget = self.widget,
            limits = self.limits,
            list_fields = list(map(lambda x: x.get_cfg(env), self.list_fields)),
            order_fields = list(map(
                                lambda x: x.get_cfg(env), self.order_fields)),
            filter_fields = list(map(
                                lambda x: x.get_cfg(env), self.filter_fields)),
        )

    async def get_items(self, env, query, fields):
        db_keys = set()
        for field in fields:
            db_keys.update(set(field.db_keys()))
        db_items = query.execute(env.db)
        stream_items = []
        for item in db_items:
            stream_item = {'id': item['id']}
            for field in fields:
                stream_item.update(field.from_db(env, self, item))
            stream_items.append(stream_item)
        return stream_items

