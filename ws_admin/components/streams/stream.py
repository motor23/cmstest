from iktomi.utils import cached_property
from ikcms.forms import Form

from ws_admin.mappers import ItemNotFound

from . import actions
from . import exc


class StreamBase:
    name = None
    title = u'Название потока'
    actions = []

    def __init__(self, component):
        assert self.name is not None
        self.component = component
        self.actions = [action(self) for action in self.actions]

    @classmethod
    def register(cls, registry):
        assert cls.name is not None
        registry[cls.name] = cls

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
            'actions': [action.get_cfg(env) for action in  self.actions],
        }


class Stream(StreamBase):
    mapper = None
    widget = 'Stream'
    max_limit = 100

    ListForm = Form
    FilterForm = Form
    ItemForm = Form

    list_fields = []
    filter_fields = []
    item_fields = []

    default_order = ['+id']

    actions = [
        actions.List,
        actions.GetItem,
        actions.NewItem,
        actions.CreateItem,
        actions.UpdateItem,
        actions.DeleteItem,
#        actions.create_draft,
#        actions.delete_draft,
#        actions.create_new_item,
#        actions.edit_item,
#        actions.get_field_block,
#        actions.set_field_value,
#        actions.delete_item,
    ]

    def __init__(self, component):
        super().__init__(component)
        assert self.mapper
        self.db_id = self.mapper.get_engine(self.component.app.db).db_id

    def tnx(self):
        return self.component.app.db(self.db_id)

    def get_list_form(self, env):
        class Form(self.ListForm):
            fields = self.list_fields
        return Form(env=env, stream=self)

    def get_filter_form(self, env):
        class Form(self.FilterForm):
            fields = self.filter_fields
        return Form(env=env, stream=self)

    def get_order_form(self, env):
        class Form(self.ListForm):
            fields = [f for f in self.list_fields if f.order]
        return Form(env=env, stream=self)

    def get_item_form(self, env, item=None, kwargs={}):
        class Form(self.ItemForm):
            fields = self.item_fields
        return Form(env=env, stream=self)

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

    def get_item(self, tnx, item_id, required=False):
        items = self.query().filter_by_id(item_id).execute(tnx)
        if not items:
            if required:
                raise exc.StreamItemNotFound(self, item_id)
            else:
                return None
        assert len(items)==1, \
               'There are {} items with id={}'.format(cnt, item_id)
        return items[0]

    def create_item(self, tnx, values):
        return self.mapper.insert(values.keys()).items([values]).execute(tnx)[0]

    def update_item(self, tnx, item_id, values):
        cnt = self.mapper.update(values.keys()).\
                            filter_by_id(item_id).\
                            values(**values).\
                            execute(tnx)
        if not cnt:
            raise exc.StreamItemNotFound(self, item_id)
        assert cnt == 1, 'There are {} items with id={}'.format(cnt, item_id)
        return values

    def delete_item(self, tnx, item_id):
        cnt = self.mapper.delete().filter_by_id(item_id).execute(tnx)
        if not cnt:
            raise exc.StreamItemNotFound(self, item_id)
        assert cnt == 1, 'There are {} items with id={}'.format(cnt, item_id)
