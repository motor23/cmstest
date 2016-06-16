from .forms.messages import MessageForm
from .forms.messages import mf_item_id
from .forms.messages import mf_filters
from .forms.messages import mf_order
from .forms.messages import mf_page
from .forms.messages import mf_page_size
from .forms.messages import mf_kwargs
from .exc import StreamNotFound
from .exc import StreamItemNotFound
from .exc import StreamLimitError
from .exc import StreamFieldNotFound
from .exc import MessageError


class Base:
    name = None

    def __init__(self, stream):
        assert self.name is not None
        self.stream = stream

    async def handle(self, env):
        raise NotImplementedError

    def get_cfg(self, env):
        return {
            'name': self.name
        }



class List(Base):
    name = 'list'

    class MessageForm(MessageForm):
        fields = [
            mf_filters,
            mf_order,
            mf_page,
            mf_page_size,
        ]

    async def handle(self, env, raw_message):
        message = self.MessageForm().to_python(raw_message)
        list_form = self.stream.get_list_form(env)
        filter_form = self.stream.get_filter_form(env)
        order_form = self.stream.get_order_form(env)

        raw_filters = message['filters']
        filters, filters_errors = filter_form.to_python(raw_filters)
        order = message['order']
        if order[1:] not in order_form:
            raise StreamFieldNotFound(self.stream, order[1:])
        page = message['page']
        page_size = message['page_size']
        
        if not (0 < page_size <= self.stream.max_limit):
            raise MessageError('Page size error')

        query = self.query(env, filters, [order])
        total = query.count(env.db)

        query = self.page_query(query, page, page_size)
        list_items = query.execute(env.db)

        raw_list_items = list_form.values_from_python(list_items)

        return {
            'stream': self.stream.name,
            'title': self.stream.title,
            'action': self.name,
            'list_fields': list_form.get_cfg(),
            'errors': filters_errors,
            'items': raw_list_items,
            'total': total,
            'filters_fields': filter_form.get_cfg(),
            'filters_errors': filters_errors,
            'filters': raw_filters,
            'page_size': page_size,
            'page': page,
            'order': message['order'],
        }

    def query(self, env, filters={}, order=['+id']):
        list_form = self.stream.get_list_form(env)
        order_form = self.stream.get_order_form(env)
        filter_form = self.stream.get_filter_form(env)

        query = self.stream.query(list_form.keys())

        for name, field in filter_form.items():
            query = field.filter(query, filters.get(name))

        for value in order:
            value, name = value[0], value[1:]
            assert name in order_form
            query = order_form[name].order(query, value)
        return query

    def page_query(self, query, page=1, page_size=1):
        assert page > 0
        assert 0 < page_size <= self.stream.max_limit
        return query.limit(page_size).offset((page-1)*page_size)




class GetItem(Base):

    name = 'get_item'

    class MessageForm(MessageForm):
        fields = [
            mf_item_id,
            mf_kwargs,
        ]

    async def handle(self, env, message):
        message = self.MessageForm().to_python(message)
        if message['item_id'] is not None:
            item = self.get_item(env, message['item_id'], required=True)
        else:
            item = {}
        item_fields_form = self.stream.get_item_form(
                                                env, item, message['kwargs'])
        raw_item = item_fields_form.from_python(item)
        return {
            'item_fields': item_fields_form.get_cfg(),
            'item': raw_item,
        }

    def get_item(self, env, item_id, required=False):
        items = self.stream.query().filter_by_id(item_id).execute(env.db)
        if not items:
            if required:
                raise StreamItemNotFound(self.stream, item_id)
            else:
                return None
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

    def get_id(self, message):
        id = message.get('id')
        if not id:
            raise FieldRequiredError('body.id')
        return id

    def get_raw_values(self, message):
        raw_values = message.get('values')
        if not isinstance(raw_values, dict):
            raise MessageError('body.values field must be the dict')

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
            raise StreamItemNotFound(self, id)
        return item


    def store(self, env, id, values):
        self.mapper.update(values.keys()).filter_by_id(id).execute(env.db)


class CreateItem(StoreBase):

    name = 'create_item'

    def get_item(self, env, id):
        item = self.stream.get_item(env, id)
        if item:
            raise StreamItemNotFound(self, id)
        return None

    def store(self, env, id, values):
        item = dict(values, id=id)
        self.mapper.insert(values.keys()).items([item]).execute(env.db)

    def filters_to_python(self, env, message):
        raw_filters = message.get('filters', {})
        if not isinstance(raw_filters, dict):
            raise MessageError('body.filters field must be the dict')
        for key in raw_filters:
            if key not in self.stream.filter_fields_dict:
                raise StreamFieldNotFound(self.stream, key)

        return self.stream.fields_accept(
            env,
            raw_filters,
            self.stream.filter_fields_dict,
        )

    def order_to_python(self, env, message):
        raw_order = message.get('order', [])
        if not isinstance(raw_order, list):
            raise MessageError('body.order field must be the list')
        if not raw_order:
            raw_order = self.stream.default_order
        for key in raw_order:
            if not isinstance(key, str):
                raise MessageError('body.order field items must be the str')
            if not (key and key[0] in ['+', '-']):
                raise MessageError(
                    'body.order field items must starts with + or -')
        return raw_order


    def limit_to_python(self, env, message):
        raw_limit = message.get('limit')
        if raw_limit not in self.stream.limits:
            raise StreamLimitError(self.stream, raw_limit)
        return raw_limit

