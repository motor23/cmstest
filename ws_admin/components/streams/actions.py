from .forms.messages import (
    MessageForm,
    mf_item_id,
    mf_filters,
    mf_order,
    mf_stream_limit,
)
from . import exc


class Base:
    name = None

    def __init__(self, stream):
        assert self.name is not None
        self.stream = stream

    async def handle(self, env): raise NotImplementedError

    def get_cfg(self, env):
        return {
            'name': self.name
        }



class List(Base):

    name = 'list'

    message_form = MessageForm([
        mf_filters,
        mf_order,
        mf_stream_limit,
    ])

    async def handle(self, env, raw_message):
        message = self.message_form.to_python(raw_message)
        list_form = self.stream.get_list_form(env)
        filter_form = self.stream.get_filter_form(env)
        order_form = self.stream.get_order_form(env)

        raw_filters = message.get('filters')
        if raw_filters:
            filters, filters_errors = filter_form.to_python(raw_filters)
        else:
            filters = filters_errors = {}

        order = message.get('order', [])
        limit = message['limit']
        if not (0 < limit < self.stream.max_limit):
            raise exc.StreamLimitError(self.stream)

        query = self.query(env, filters, order, limit)
        count_list_items = query.count(env.db)
        list_items = query.execute(env.db)

        raw_list_items = list_form.values_from_python(list_items)

        return {
            'stream': self.stream.name,
            'action': self.name,
            'list_fields': list_form.get_cfg(),
            'list_items': raw_list_items,
            'count_list_items': count_list_items,
            'filter_fields': filter_form.get_cfg(),
            'filters_errors': filters_errors,
        }

    def query(self, env, filters={}, order=[], limit=None):
        assert 0 < limit <= self.stream.max_limit
        list_form = self.stream.get_list_form(env)
        order_form = self.stream.get_order_form(env)
        filter_form = self.stream.get_filter_form(env)

        query = self.stream.query(list_form.keys())

        for name, field in filter_form.items():
            query = field.filter(query, filters.get(name))

        for key in order or ['+id']:
            value, name = key[0], key[1:]
            query = order_form[name].order(query, value)
        return query.limit(limit)



class GetItem(Base):

    name = 'get_item'

    message_form = MessageForm([
        mf_item_id,
    ])

    async def handle(self, env, message):
        message = self.message_form.to_python(message)
        item_id = message.get('item_id')
        if item_id is not None:
            item = self.get_item(env, item_id, required=True)
        else:
            item = {}
        item_fields_form = self.stream.get_item_form(env, item)
        raw_item = item_fields_form.from_python(item)
        return {
            'item_fields': item_fields_form.get_cfg(),
            'item': raw_item,
        }

    def get_item(self, env, item_id, required=False):
        items = self.stream.query().filter_by_id(item_id).execute(env.db)
        if not items and required:
            raise exc.StreamItemNotFound(self.stream, item_id)
        return items[0]


class StoreBase(Base):

    async def handle(self, env, message):
        id = self.get_id(message)
        raw_values = self.get_raw_values(message)
        item = self.get_item(env, id)
        item_fields = self.stream.get_item_fields(env, item)
        values, errors = self.accept(env, raw_values, item_fields)
        self.store(env, id, values)
        return {
            'fields': self.stream.get_fields_cfg(env, item_fields),
            'values': raw_values,
            'errors': errors,
        }

    def get_id(self, maessage):
        id = message.get('id')
        if not id:
            raise exc.FieldRequiredError('body.id')
        return id

    def get_raw_values(self, message):
        raw_values = message.get('values')
        if not isinstance(values, dict):
            raise exc.MessageError('body.values field must be the dict')

    def get_item(self, env, id):
        raise NotImplementedError

    def accept(self, env, raw_values, item_fields):
        return self.stream.item_accept(env, raw_values, item_fields)

    def store(self, env, values):
        raise NotImplementedError



class UpdateItem(StoreBase):

    name = 'update_item'

    def get_item(self, env, id):
        item = self.stream.get_item(env, id)
        if not item:
            raise exc.StreamItemNotFound(self, id)
        return item


    def store(self, env, id, values):
        self.mapper.update(values.keys()).filter_by_id(id).execute(env.db)


class CreateItem(StoreBase):

    name = 'create_item'

    def get_item(self, env, id):
        item = self.stream.get_item(env, id)
        if item:
            raise exc.StreamItemNotFound(self, id)
        return None

    def store(self, env, id, values):
        item = dict(values, id=id)
        self.mapper.insert(values.keys()).items([item]).execute(env.db)

