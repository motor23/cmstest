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

    async def handle(self, env, message):
        filters, filters_errors = self.filters_to_python(env, message)
        order = self.order_to_python(env, message)
        limit = self.limit_to_python(env, message)
        offset = self.offset_to_python(env, message)

        query = self.query(filters, order, limit)
        total = query.count(env.db)
        list_items = query.offset(offset).execute(env.db)

        raw_list_items = self.stream.fields_from_python(
            env,
            list_items,
            self.stream.list_fields_dict,
        )

        return {
            'stream': self.stream.name,
            'title': self.stream.title,
            'action': self.name,
            'items': raw_list_items,
            'total': total,
            'limit': limit,
            'offset': offset,
            'filters': message.get('filters', {}),
            'errors': filters_errors,
        }

    def query(self, filters, order, limit, offset=0):
        query = self.stream.query(self.stream.list_fields_dict.keys())

        for name, field in self.stream.filter_fields_dict.items():
            query = field.filter(query, filters.get(name))

        for key in order:
            value, name = key[0], key[1:]
            query = self.stream.list_fields_dict[name].order(query, value)

        if offset > 0:
            query = query.offset(offset)

        return query.limit(limit)

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

    def offset_to_python(self, env, message):
        raw_offset = message.get('offset', 0)
        return raw_offset
