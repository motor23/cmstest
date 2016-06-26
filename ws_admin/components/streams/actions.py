from ikcms.ws_apps.base.forms import MessageForm as MessageFormBase

from .forms import message_fields
from . import exc


class Base:
    name = None

    def __init__(self, stream):
        assert self.name is not None
        self.stream = stream

    async def handle(self, env, message):
        raise NotImplementedError

    def get_cfg(self, env):
        return {
            'name': self.name
        }



class List(Base):
    name = 'list'

    class MessageForm(MessageFormBase):
        fields = [
            message_fields.filters,
            message_fields.order,
            message_fields.page,
            message_fields.page_size,
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
            raise exc.StreamFieldNotFound(self.stream, order[1:])
        page = message['page']
        page_size = message['page_size']

        if not 0 < page_size <= self.stream.max_limit:
            raise exc.MessageError('Page size error')
        db = await env.app.db(self.stream.mapper.db_id)
        async with await db.begin():
            query = self.query(env, filters, [order])
            total = await query.count(db)

            query = self.page_query(query, page, page_size)
            list_items = await query.execute(db)

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

    def query(self, env, filters=None, order=None):
        filters = filters or {}
        order = order or ['+id']

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

    class MessageForm(MessageFormBase):
        fields = [
            message_fields.item_id,
        ]

    async def handle(self, env, message):
        message = self.MessageForm().to_python(message)
        db = await env.app.db(self.stream.mapper.db_id)
        async with await db.begin():
            item = await self.stream.get_item(
                db, message['item_id'],
                required=True,
            )
        item_fields_form = self.stream.get_item_form(env, item=item)
        raw_item = item_fields_form.from_python(item)
        return {
            'item_fields': item_fields_form.get_cfg(),
            'item': raw_item,
        }


class NewItem(Base):

    name = 'new_item'

    class MessageForm(MessageFormBase):
        fields = [
            message_fields.kwargs,
        ]

    async def handle(self, env, message):
        message = self.MessageForm().to_python(message)
        item_fields_form = self.stream.get_item_form(
            env, kwargs=message['kwargs'])
        raw_item = item_fields_form.from_python(item_fields_form.get_initials())
        return {
            'item_fields': item_fields_form.get_cfg(),
            'item': raw_item,
        }


class CreateItem(Base):

    name = 'create_item'

    class MessageForm(MessageFormBase):
        fields = [
            message_fields.values,
            message_fields.kwargs,
        ]

    async def handle(self, env, message):
        item_fields_form = self.stream.get_item_form(
            env, kwargs=message['kwargs'])
        raw_item = message['values']
        item, errors = item_fields_form.to_python(raw_item)
        if not errors:
            db = await env.app.db(self.stream.mapper.db_id)
            async with await db.begin():
                item = await self.stream.create_item(db, item)
            raw_item = item_fields_form.from_python(item)
        return {
            'item_fields': item_fields_form.get_cfg(),
            'item': raw_item,
            'errors': errors,
        }


class UpdateItem(Base):

    name = 'update_item'

    class MessageForm(MessageFormBase):
        fields = [
            message_fields.item_id,
            message_fields.values,
        ]

    async def handle(self, env, message):
        item_fields_form = self.stream.get_item_form(env)
        item_id = message['item_id']
        raw_values = message['values']
        values, errors = item_fields_form.to_python(raw_values,
                                                    keys=raw_values.keys())
        if not errors:
            db = await env.app.db(self.stream.mapper.db_id)
            async with await db.begin():
                item = await self.stream.update_item(db, item_id, values)
            raw_item = item_fields_form.from_python(item, keys=item.keys())
        return {
            'item_fields': item_fields_form.get_cfg(),
            'item': raw_item,
            'errors': errors,
        }


class DeleteItem(Base):

    name = 'delete_item'

    class MessageForm(MessageFormBase):
        fields = [
            message_fields.item_id,
        ]

    async def handle(self, env, message):
        db = await env.app.db(self.stream.mapper.db_id)
        async with await db.begin():
            await self.stream.delete_item(db, message['item_id'])
        return {
            'item_id': message['item_id'],
        }

