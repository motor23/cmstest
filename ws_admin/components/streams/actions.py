from .exc import (
    StreamLimitError,
    StreamFieldNotFound,
    MessageError,
)

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

    async def handle(self, env, message):
        filters, filters_errors = self.filters_to_python(env, message)
        limit = self.limit_to_python(env, message)

        query = self.query(filters, limit)
        count_list_items = query.count(env.db)
        list_items = query.execute(env.db)

        raw_list_items = self.stream.fields_from_python(
            env,
            list_items,
            self.stream.list_fields_dict,
        )

        return {
            'stream': self.stream.name,
            'action': self.name,
            'list_items': raw_list_items,
            'count_list_items': count_list_items,
            'filters': message.get('filters', {}),
            'filters_errors': filters_errors,
        }

    def query(self, filters, limit):
        query = self.stream.query(self.stream.list_fields_dict.keys())

        for name, value in filters.items():
            query = self.stream.filter_fields_dict[name].filter(query, value)

        return query.limit(limit)


    def filters_to_python(self, env, message):
        raw_filters = message.get('filters', {})
        if not isinstance(raw_filters, dict):
            raise MessageError('body.filters field must be the dict')
        return self.stream.fields_accept(
            env,
            raw_filters,
            self.stream.filter_fields_dict,
        )

    def limit_to_python(self, env, message):
        raw_limit = message.get('limit')
        if raw_limit not in self.stream.limits:
            raise StreamLimitError(self.stream, raw_limit)
        return raw_limit

