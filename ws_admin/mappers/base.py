from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.orm import ColumnProperty, RelationshipProperty
from sqlalchemy import sql, func


class ItemNotFoundError(Exception):
    pass


class Query:

    def __init__(self, mapper, keys=None, query=None, items=None):
        self._mapper = mapper
        self._table_keys, self._relation_keys = mapper.div_keys(keys)
        self._keys = keys
        if query is None:
            self.set_query()
        else:
            self._query = query
        if items is None:
            self._items = None
        else:
            self._items = items.copy()

    def set_query(self, query=None):
        raise NotImplementedError

    def clone(self, keys=None, query=None, items=None):
        if keys is None:
            keys = self._keys
        if query is None:
            query = self._query
        if items is None:
            items = self._items
        return self.__class__(
            self._mapper,
            keys=keys,
            query=query,
            items=items,
        )

    def items(self, items):
        return self.clone(items=(self._items or []) + items)

    def execute(self, db):
        if self._items is None:
            return self._execute_query(db)
        else:
            return self._execute_items(db)

    __call__ = execute

    def _execute_query(self, db):
        raise NotImplementedError

    def _execute_items(self, db):
        raise NotImplementedError

    def filter_by_id(self, *ids):
        return self.filter('id', 'in', ids)

    def filter_by(self, **kwargs):
        q = self.clone()
        for key, value in kwargs.items():
            q = q.filter(key, '==', value)
        return q

    def filter(self, key, op, value):
        assert self._items is None
        column = self._mapper.table.c[key]
        if op == '==':
            condition = column == value
        elif op == '!=':
            condition = column != value
        elif op == '>':
            condition = column > value
        elif op == '>=':
            condition = column >= value
        elif op == '<':
            condition = column < value
        elif op == '<=':
            condition = column <= value
        elif op == 'in':
            condition = column.in_(value)
        elif op == 'like':
            condition = column.like("%" + value + "%")
        else:
            raise ValueError('Uncnown operator {}'.format(op))
        return self._add_condition(condition)

    def _add_condition(self, condition):
        return self.clone(query=self._query.where(condition))


class SelectQuery(Query):

    def set_query(self, query=None):
        columns = [self._mapper.table.c[key] for key in self._table_keys]
        self._query = sql.select(columns)

    def order_by(self, *keys):
        columns = []
        for key in keys:
            if key.startswith('-'):
                columns.append(self._mapper.table.c[key[1:]].desc())
            else:
                if key.startswith('+'):
                    key = key[1:]
                columns.append(self._mapper.table.c[key])
        return self.clone(query=self._query.order_by(*columns))

    def limit(self, value):
        return self.clone(query=self._query.limit(value))

    def offset(self, value):
        return self.offset(query=self._query.offset(value))

    def count(self, db):
        columns = [func.count(self._mapper.table.c.id)]
        return db.execute(self._query.with_only_columns(columns)).fetchone()[0]

    def set_keys(self, keys):
        columns = [self._mapper.table.c[key] for key in self._table_keys]
        query = self._query.with_only_columns(columns)
        return self.clone(keys=keys, query=query)

    def __getitem__(self, key):
        if isinstance(key, slice):
            limit = key.max - key.min
            offset = key.min
        elif isinstance(key, int):
            limit = 1
            offset = key
        else:
            raise TypeError(type(key))
        return self.limit(limit).offset(offset)

    def _execute_query(self, db):
        result = [dict(row) for row in db.execute(self._query)]
        row_by_id = dict(((row['id'], row) for row in result))
        ids = [item['id'] for item in result]
        for key in self._relation_keys:
            for id, value in self._mapper.relations[key].load(db, ids).items():
                row_by_id[id][key] = value
        return result

    def _execute_items(self, db):
        assert not [item for item in self._items if 'id' not in item]
        ids = [item['id'] for item in self._items]
        query = self._query.where(self._mapper.table.c.id.in_(ids))
        result = [dict(row) for row in db.execute(query)]
        row_by_id = dict(((row['id'], row) for row in result))
        for item in self._items:
            row = row_by_id.get(item['id'])
            if row is None:
                raise ItemNotFoundError(item['id'])
            item.update(row)
        return self._items


class InsertQuery(Query):

    def set_query(self, query=None):
        self._query = self._mapper.table.insert()

    def _execute_items(self, db):
        for item in self._items:
            table_value = dict([(key, item[key]) for key in self._table_keys])
            result = db.execute(self._query.values(**table_value))
            item['id'] = result.lastrowid
            for key in self._relation_keys:
                self._mapper.relations[key].store(db, item['id'], item[key])
        return self._items


class UpdateQuery(Query):

    def set_query(self, query=None):
        self._query = self._mapper.table.update()

    def values(self, **values):
        return self.clone(query=self._query.values(**values))

    def _execute_items(self, db):
        assert not [item for item in self._items if 'id' not in item]
        for item in self._items:
            query = self._query.where(self._mapper.table.c.id == item['id'])
            value = dict([(key, item[key]) for key in self._table_keys])
            result = db.execute(query.values(**value))
            if result.rowcount != 1:
                raise ItemNotFoundError(item['id'])
            for key in self._relation_keys:
                self._mapper.relations[key].store(db, item['id'], item[key])
        return len(self._items)

    def _execute_query(self, db):
        return db.execute(self._query).rowcount


def model_to_mapper(model):
    relations = {}
    for name in dir(model):
        attr = getattr(model, name)
        if isinstance(attr, InstrumentedAttribute):
            prop = attr.property
            if isinstance(prop, ColumnProperty):
                pass
            elif isinstance(prop, RelationshipProperty):
                if prop.secondaryjoin is None:
                    pass
                else:
                    local1, remote1 = prop.local_remote_pairs[0]
                    local2, remote2 = prop.local_remote_pairs[1]
                    order_field = remote1.table.c.get('order')
                    relations[prop.key] = M2MRelation(
                        local1, remote1, remote2, local2
                    )
    return Mapper(model.__table__, relations)


class Mapper:

    table = None
    relations = {}

    SelectQuery = SelectQuery
    InsertQuery = InsertQuery
    UpdateQuery = UpdateQuery

    def __init__(self, table, relations):
        relations = relations or {}
        self.table = table
        self.relations = relations.copy()
        self.allowed_keys = set(list(self.table.c.keys()) + list(self.relations))

    def div_keys(self, keys=None):
        if keys is None:
            keys = self.allowed_keys
        else:
            keys = set(keys)
            error_keys = keys - self.allowed_keys
            assert not error_keys, 'Unknown fields {}'.format(error_keys)
        table_keys = set([key for key in keys if key in self.table.c])
        table_keys.add('id')
        relation_keys = set([key for key in keys if key in self.relations])
        return table_keys, relation_keys

    def select(self, keys=None):
        return self.SelectQuery(self, keys)

    def insert(self, keys=None):
        return self.InsertQuery(self, keys)

    def update(self, values, keys=None):
        return self.UpdateQuery(self, values)

    def load(self, db, items, keys=None):
        return self.select(keys).items(items).execute(db)

    def store(self, db, items, keys=None):
        self.div_keys(keys)  # check keys is allowed
        ids = [item.get('id') for item in items]
        ids = set([id for id in ids if id is not None])
        result = self.select(['id']).filter_by_id(*ids).execute(db)
        update_ids = set([item['id'] for item in result])
        ins_items = [item for item in items if item.get('id') not in update_ids]
        up_items = [item for item in items if item.get('id') in items]
        self.insert(keys).items(ins_items).execute(db)
        self.update(keys).items(up_items).execute(db)


class M2MRelation:

    def __init__(self, local_field,
                 rel_local_field, rel_remote_field,
                 remote_field,
                 order_field=None):
        self.local_field = local_field
        self.rel_local_field = rel_local_field
        self.rel_remote_field = rel_remote_field
        self.remote_field = remote_field
        self.local_table = local_field.table
        self.rel_table = rel_local_field.table
        self.remote_table = remote_field.table
        self.order_field = order_field

    def load(self, db, ids):
        result = {}
        for id, remote_id in db.execute(self.select_query(ids)):
            result.setdefault(id, []).append(remote_id)
        return result

    def store(self, db, id, value):
        db.execute(self.delete_query(id))
        for num, rel_id in enumerate(value):
            order = self.order_field and (num+1) or None
            db.execute(self.insert_query(id, rel_id, order=order))

    def select_query(self, ids):
        s = sql.select([self.rel_local_field, self.rel_remote_field]) \
            .where(self.rel_local_field.in_(ids))
        if self.order_field:
            s = s.order_by(self.order_field)
        return s

    def delete_query(self, local_id):
        return sql.delete(self.rel_table) \
            .where(self.rel_local_field == local_id)

    def insert_query(self, local_id, remote_id, order=None):
        values = {
            self.rel_local_field.key: local_id,
            self.rel_remote_field.key: remote_id,
        }
        if order:
            values[self.order_field.key] = order
        return sql.insert(self.rel_table).values(**values)


