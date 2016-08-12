from unittest import TestCase
from unittest import skipIf
from unittest.mock import MagicMock
from datetime import date

import sqlalchemy as sa

from ikcms.ws_components.db import component
from ikcms import orm
from ikcms.orm import exc
from ikcms.utils.asynctests import asynctest

from tests.cfg import cfg
from tests.models import create_models1, create_models2, create_metadata


DB_URL1 = cfg.MYSQL_URL or cfg.POSTGRESS_URL
DB_URL2 = cfg.MYSQL_URL2 or cfg.POSTGRESS_URL2


@skipIf(not DB_URL1, 'db url undefined')
class BaseMapperTestCase(TestCase):

    item1 = {
            'id': 1,
            'title': '111t',
            'title2': '111t2',
            'date': date(2005, 4, 20),
    }
    item2 = {
            'id': 2,
            'title': '222t',
            'title2': '222t2',
            'date': date(1998, 7, 6),
    }
    item3 = {
            'id': 3,
            'title': '333t',
            'title2': '333t2',
            'date': date(2016, 12, 12),
    }
    item4 = {
            'id': 4,
            'title': '444t',
            'title2': '444t2',
            'date': date(2020, 1, 17),
    }
    items = [item1, item2, item3, item4]
    items_table_keys = {'id', 'title', 'title2', 'date'}
    items_relation_keys = set()
    items_allowed_keys = items_table_keys.union(items_relation_keys)
    mapper_cls = orm.mappers.Base

    class CustomMapperClass(mapper_cls):

        name = 'CustomTest'

        def create_columns(self):
            return [
                sa.Column('title', sa.String(255)),
                sa.Column('title2', sa.String(255)),
            ]


    async def asetup(self):
        self.models1 = create_models1()
        self.models2 = create_models2()
        registry = orm.mappers.Registry(
            create_metadata([self.models1, self.models2]))
        self.mapper_cls.from_model(registry, [self.models1.Test])

        app = MagicMock()
        del app.db
        app.cfg.DATABASES = {
            'db1': DB_URL1,
            'db2': DB_URL2,
        }

        Component = component(mappers=registry)

        db = await Component.create(app)
        async with await db() as session:
            conn1 = await session.get_connection(db.engines['db1'])
            await self.models1.reset(conn1)
            conn2 = await session.get_connection(db.engines['db2'])
            await self.models2.reset(conn2)
        return {
            'db': db,
        }

    async def aclose(self, db):
        db.close()

    @asynctest
    async def test_init(self, db):
        mapper = db.mappers['db1']['Test']
        self.assertEqual(mapper.registry, db.mappers)
        self.assertEqual(mapper.db_id, 'db1')
        self.assertEqual(mapper.table_keys, self.items_table_keys)
        self.assertEqual(mapper.relation_keys, self.items_relation_keys)
        self.assertEqual(mapper.allowed_keys, self.items_allowed_keys)

    @asynctest
    async def test_div_keys(self, db):
        mapper = db.mappers['db1']['Test']
        table_keys, relation_keys = mapper.div_keys()
        self.assertEqual(table_keys, self.items_table_keys)
        self.assertEqual(relation_keys, self.items_relation_keys)
        table_keys, relation_keys = mapper.div_keys(['title', 'title2'])
        self.assertEqual(table_keys, {'title', 'title2'})
        self.assertEqual(relation_keys, set())

    @asynctest
    async def test_create_table(self, db):
        self.CustomMapperClass.create(db.mappers, db_id='db1')
        db.mappers.create_schema()
        async with await db() as session:
            conn1 = await session.get_connection(db.engines['db1'])
            await self.models1.reset(conn1)
        self.assertEqual(
            db.mappers.metadata['db1'].tables['CustomTest'].c.keys(),
            ['id', 'title', 'title2'],
        )
        self.assertEqual(
            db.mappers['db1']['CustomTest'].table,
            db.mappers.metadata['db1'].tables['CustomTest'],
        )

    @asynctest
    async def test_select(self, db):
        mapper = db.mappers['db1']['Test']
        query = mapper.query()
        async with await db() as session:
            q = sa.sql.insert(self.models1.test_table1).values(self.items)
            result = await session.execute(q)

            # ids arg
            items = await query.id(2, 4).select_items(session)
            self.assertEqual(items, [self.item2, self.item4])
            items = await query.id(2, 4).select_items(session, keys=['title'])
            self.assertEqual(items, [
                {'id': 2, 'title': '222t'},
                {'id': 4, 'title': '444t'},
            ])

            # query arg
            _query = query.filter_by(title='333t')
            items = await _query.select_items(session)
            self.assertEqual(items, [self.item3])

            items = await _query.select_items(session, keys=['title2'])
            self.assertEqual(items, [{'id': 3, 'title2': '333t2'}])

            # ids and query args
            items = await query.id(4,2).select_items(session)
            self.assertEqual(items, [self.item2, self.item4])

            _query = query.filter_by(title='333t').id(44)
            items = await _query.select_items(session)
            self.assertEqual(items, [])

    @asynctest
    async def test_insert(self, db):
        mapper = db.mappers['db1']['Test']
        _item1 = dict(self.item1, title2=None, date=None)
        _item4 = dict(self.item4, id=None)

        query = mapper.query().order_by(mapper.c['id'])
        async with await db() as session:
            result = await query.insert_item(session, self.item3)
            self.assertEqual(result, self.item3)
            items = await query.select_items(session)
            self.assertEqual(items, [self.item3])

            result = await query.insert_item(
                session, self.item1, keys=['id', 'title'])
            self.assertEqual(result, self.item1)
            items = await query.select_items(session)
            self.assertEqual(items, [_item1, self.item3])

            result = await query.insert_item(session, _item4)
            self.assertEqual(result, self.item4)
            items = await query.select_items(session)
            self.assertEqual(items, [_item1, self.item3, self.item4])

            with self.assertRaises(Exception): # XXX Exception??
                await mapper.insert_item(session, item3)

    @asynctest
    async def test_update(self, db):
        mapper = db.mappers['db1']['Test']
        query = mapper.query().order_by(mapper.c['id'])
        async with await db() as session:
            q = sa.sql.insert(self.models1.test_table1).values(self.items)
            result = await session.execute(q)
            # test without 'keys' key arg
            _item2 = dict(self.item2, title='updated')
            item = await query.update_item(session, 2, _item2)
            self.assertEqual(item, _item2)
            items = await query.id(2).select_items(session)
            self.assertEqual(items, [_item2])
            items = await query.id(1, 2, 3, 4).select_items(session)
            self.assertEqual(items, [
                self.item1,
                _item2,
                self.item3,
                self.item4,
            ])
            # test with 'keys' key arg
            _item4 = dict(self.item4, title2='updated2')
            item = await query.update_item(
                session,
                4,
                {'title2': 'updated2'},
                keys = ['title2'],
            )
            self.assertEqual(item, {'id':4, 'title2': 'updated2'})
            items = await query.id(4).select_items(session)
            self.assertEqual(items, [_item4])
            items = await query.id(1, 2, 3, 4).select_items(session)
            self.assertEqual(items, [
                self.item1,
                _item2,
                self.item3,
                _item4,
            ])
            query = query.filter_by(title='zzz')
            with self.assertRaises(exc.ItemNotFoundError) as e:
                await query.update_item(
                    session,
                    4,
                    {'id':4, 'title2': 'updated2'},
                    keys=['title2'],
                )
                self.assertEqual(e.args[0], 4)

    @asynctest
    async def test_delete(self, db):
        mapper = db.mappers['db1']['Test']
        query = mapper.query().order_by(mapper.c['id'])
        async with await db() as session:
            q = sa.sql.insert(self.models1.test_table1).values(self.items)
            result = await session.execute(q)
            # id arg
            await query.delete_item(session, 2)
            self.assertEqual(await query.id(2).select_items(session), [])
            with self.assertRaises(exc.ItemNotFoundError) as e:
                await query.delete_item(session, 2)
            self.assertEqual(e.exception.args[0], 2)
            items = await query.id(1, 3, 4).select_items(session)
            self.assertEqual(items, [self.item1, self.item3, self.item4])
            _query = query.filter_by(title='zzz').id(4)
            items = await _query.select_items(session)
            self.assertEqual(items, [])

            await query.delete_item(session, 4)
            items = await query.select_items(session)
            self.assertEqual(items, [self.item1,  self.item3])

    @asynctest
    async def test_count(self, db):
        mapper = db.mappers['db1']['Test']
        query = mapper.query()
        async with await db() as session:
            result = await query.count_items(session)
            self.assertEqual(result, 0)

            q = sa.sql.insert(self.models1.test_table1).values(self.items)
            await session.execute(q)
            result = await query.count_items(session)
            self.assertEqual(result, len(self.items))
            result = await query.filter_by(id=1).count_items(session)
            self.assertEqual(result, 1)



@skipIf(not DB_URL1, 'db url undefined')
class I18nMapperTestCase(TestCase):

    item1 = {
            'id': 1,
            'title': '111t',
            'title2': '111t2',
    }
    item2 = {
            'id': 2,
            'title': '222t',
            'title2': '222t2',
    }
    item3 = {
            'id': 3,
            'title': '333t',
            'title2': '333t2',
    }
    item4 = {
            'id': 4,
            'title': '444t',
            'title2': '444t2',
    }
    items = [item1, item2, item3, item4]
    items_table_keys = {'id', 'title', 'title2'}
    items_relation_keys = set()
    items_allowed_keys = items_table_keys.union(items_relation_keys)

    class I18nMapperClass(orm.mappers.I18n):

        name = 'Test'
        common_keys = ['title']

        def create_columns(self):
            return [
                sa.Column('title', sa.String(255)),
                sa.Column('title2', sa.String(255)),
            ]

    async def asetup(self):
        self.models1 = create_models1()
        registry = orm.mappers.Registry(create_metadata([self.models1]))

        self.I18nMapperClass.create(registry, db_id='db1')
        registry.create_schema()

        app = MagicMock()
        del app.db
        app.cfg.DATABASES = {
            'db1': DB_URL1,
            'db2': DB_URL2,
        }

        Component = component(mappers=registry)

        db = await Component.create(app)
        async with await db() as session:
            conn1 = await session.get_connection(db.engines['db1'])
            await self.models1.reset(conn1)
        return {
            'db': db,
        }

    async def aclose(self, db):
        db.close()

    @asynctest
    async def test_create_table(self, db):
        self.assertEqual(
            db.mappers.metadata['db1'].tables['TestRu'].c.keys(),
            ['id', 'state', 'title', 'title2'],
        )
        self.assertEqual(
            db.mappers.metadata['db1'].tables['TestEn'].c.keys(),
            ['id', 'state', 'title', 'title2'],
        )
        self.assertEqual(
            db.mappers['db1']['ru']['Test'].table,
            db.mappers.metadata['db1'].tables['TestRu'],
        )
        self.assertEqual(
            db.mappers['db1']['en']['Test'].table,
            db.mappers.metadata['db1'].tables['TestEn'],
        )

    @asynctest
    async def test_insert(self, db):
        mapper_ru = db.mappers['db1']['ru']['Test']
        mapper_en = db.mappers['db1']['en']['Test']
        query_ru = mapper_ru.query().order_by(mapper_ru.c['id'])
        query_en = mapper_en.query().order_by(mapper_en.c['id'])
        query_ru_abs = mapper_ru.absent_query().order_by(mapper_ru.c['id'])
        query_en_abs = mapper_en.absent_query().order_by(mapper_en.c['id'])


        _item1_ru = dict(self.item1, state='normal')
        _item1_en = dict(self.item1, state='absent', title2=None)

        _item2_ru = dict(self.item2, state='absent', title2=None)
        _item2_en = dict(self.item2, state='normal')

        _item4_ru = dict(self.item4, state='normal')
        _item4_en = dict(self.item4, state='absent', title2=None)

        _item3_ru = dict(self.item3, state='absent', title2=None)
        _item3_en = dict(self.item3, state='normal')

        async with await db() as session:
            result = await query_ru.insert_item(
                session,
                dict(self.item1, id=None),
            )
            await session.commit()
            self.assertEqual(result, _item1_ru)
            items = await query_ru.select_items(session)
            self.assertEqual(items, [_item1_ru])
            items = await query_ru_abs.select_items(session)
            self.assertEqual(items, [])
            items = await query_en.select_items(session)
            self.assertEqual(items, [])
            items = await query_en_abs.select_items(session)
            self.assertEqual(items, [_item1_en])

            result = await query_en.insert_item(
                session,
                dict(self.item2, id=None),
            )
            await session.commit()
            self.assertEqual(result, _item2_en)
            items = await query_en.select_items(session)
            self.assertEqual(items, [_item2_en])
            items = await query_en_abs.select_items(session)
            self.assertEqual(items, [_item1_en])
            items = await query_ru.select_items(session)
            self.assertEqual(items, [_item1_ru])
            items = await query_ru_abs.select_items(session)
            self.assertEqual(items, [_item2_ru])

            result = await query_ru.insert_item(session, self.item4)
            await session.commit()
            self.assertEqual(result, _item4_ru)
            items = await query_ru.select_items(session)
            self.assertEqual(items, [_item1_ru, _item4_ru])
            items = await query_ru_abs.select_items(session)
            self.assertEqual(items, [_item2_ru])
            items = await query_en.select_items(session)
            self.assertEqual(items, [_item2_en])
            items = await query_en_abs.select_items(session)
            self.assertEqual(items, [_item1_en, _item4_en])

            result = await query_en.insert_item(session, self.item3)
            await session.commit()
            self.assertEqual(result, _item3_en)
            items = await query_en.select_items(session)
            self.assertEqual(items, [_item2_en,_item3_en])
            items = await query_en_abs.select_items(session)
            self.assertEqual(items, [_item1_en, _item4_en])
            items = await query_ru.select_items(session)
            self.assertEqual(items, [_item1_ru, _item4_ru])
            items = await query_ru_abs.select_items(session)
            self.assertEqual(items, [_item2_ru, _item3_ru])


    @asynctest
    async def test_create_i18n_version(self, db):
        mapper_ru = db.mappers['db1']['ru']['Test']
        mapper_en = db.mappers['db1']['en']['Test']
        query_ru = mapper_ru.query().order_by(mapper_ru.c['id'])
        query_en = mapper_en.query().order_by(mapper_en.c['id'])
        async with await db() as session:
            await query_ru.insert_item(session, self.item1)
            await mapper_en.i18n_create_version(session, self.item1['id'])
            cnt = await query_ru.count_items(session)
            self.assertEqual(cnt, 1)
            cnt = await query_en.count_items(session)
            self.assertEqual(cnt, 1)
            await query_en.insert_item(session, self.item2)
            await mapper_ru.i18n_create_version(session, self.item2['id'])
            cnt = await query_ru.count_items(session)
            self.assertEqual(cnt, 2)
            cnt = await query_en.count_items(session)
            self.assertEqual(cnt, 2)


    @asynctest
    async def test_update_item(self, db):
        mapper_ru = db.mappers['db1']['ru']['Test']
        mapper_en = db.mappers['db1']['en']['Test']
        query_ru = mapper_ru.query().order_by(mapper_ru.c['id'])
        query_en = mapper_en.query().order_by(mapper_en.c['id'])

        async with await db() as session:
            await query_ru.insert_item(session, self.item1)
            await mapper_en.i18n_create_version(session, self.item1['id'])
            await query_ru.insert_item(session, self.item2)
            await mapper_en.i18n_create_version(session, self.item2['id'])
            item1_ru = dict(self.item1, state='normal')
            item2_ru = dict(self.item2, state='normal')
            item1_en = dict(self.item1, title2=None, state='normal')
            item2_en = dict(self.item2, title2=None, state='normal')
            values = {'title': 'updated_title', 'title2': 'updated_title2'}
            await query_ru.update_item(session, item1_ru['id'], values=values);
            item1_ru.update(values)
            item1_en['title'] = values['title']
            items = await query_ru.select_items(session)
            self.assertEqual(items, [item1_ru, item2_ru])
            items = await query_en.select_items(session)
            self.assertEqual(items, [item1_en, item2_en])

            values = {'title': 'en_updated_title', 'title2': 'en_updated_title2'}
            await query_en.update_item(session, item2_en['id'], values=values);
            item2_en.update(values)
            item2_ru['title'] = values['title']
            items = await query_ru.select_items(session)
            self.assertEqual(items, [item1_ru, item2_ru])
            items = await query_en.select_items(session)
            self.assertEqual(items, [item1_en, item2_en])

    @asynctest
    async def test_delete_item(self, db):
        mapper_ru = db.mappers['db1']['ru']['Test']
        mapper_en = db.mappers['db1']['en']['Test']
        query_ru = mapper_ru.query().order_by(mapper_ru.c['id'])
        query_en = mapper_en.query().order_by(mapper_en.c['id'])
        abs_query_en = mapper_en.absent_query().order_by(mapper_en.c['id'])

        async with await db() as session:
            await query_ru.insert_item(session, self.item1)
            await mapper_en.i18n_create_version(session, self.item1['id'])
            await query_ru.insert_item(session, self.item2)
            await mapper_en.i18n_create_version(session, self.item2['id'])
            item1_ru = dict(self.item1, state='normal')
            item2_ru = dict(self.item2, state='normal')
            item1_en = dict(self.item1, title2=None, state='normal')
            item2_en = dict(self.item2, title2=None, state='normal')
            await query_ru.delete_item(session, item1_ru['id'])
            items = await query_ru.select_items(session)
            self.assertEqual(items, [item2_ru])
            items = await query_en.select_items(session)
            self.assertEqual(items, [item2_en])
            await query_en.delete_item(session, item2_en['id'])
            items = await query_ru.select_items(session)
            self.assertEqual(items, [])
            items = await query_en.select_items(session)
            self.assertEqual(items, [])

            await query_ru.insert_item(session, self.item1)
            await query_ru.insert_item(session, self.item2)
            item1_ru = dict(self.item1, state='normal')
            item2_ru = dict(self.item2, state='normal')
            item1_en = dict(self.item1, title2=None, state='absent')
            item2_en = dict(self.item2, title2=None, state='absent')

            await query_ru.delete_item(session, item1_ru['id'])
            items = await query_ru.select_items(session)
            self.assertEqual(items, [item2_ru])
            items = await abs_query_en.select_items(session)
            self.assertEqual(items, [item2_en])
            await abs_query_en.delete_item(session, item2_en['id'])
            items = await query_ru.select_items(session)
            self.assertEqual(items, [])
            items = await abs_query_en.select_items(session)
            self.assertEqual(items, [])



@skipIf(not (DB_URL1 and DB_URL2), 'db url or db urk2 undefined')
class PubMapperTestCase(TestCase):

    item1 = {
            'id': 1,
            'title': '111t',
            'title2': '111t2',
    }
    item2 = {
            'id': 2,
            'title': '222t',
            'title2': '222t2',
    }
    item3 = {
            'id': 3,
            'title': '333t',
            'title2': '333t2',
    }
    item4 = {
            'id': 4,
            'title': '444t',
            'title2': '444t2',
    }
    items = [item1, item2, item3, item4]
    items_table_keys = {'id', 'title', 'title2'}
    items_relation_keys = set()
    items_allowed_keys = items_table_keys.union(items_relation_keys)

    class PubMapperClass(orm.mappers.Pub):

        name = 'PubTest'

        def create_columns(self):
            return [
                sa.Column('title', sa.String(255)),
                sa.Column('title2', sa.String(255)),
            ]

    async def asetup(self):
        self.models1 = create_models1()
        self.models2 = create_models2()
        registry = orm.mappers.Registry({
            'admin': self.models1.metadata,
            'front': self.models2.metadata,
        })

        self.PubMapperClass.create(registry)
        registry.create_schema()

        app = MagicMock()
        del app.db
        app.cfg.DATABASES = {
            'admin': DB_URL1,
            'front': DB_URL2,
        }

        Component = component(mappers=registry)

        db = await Component.create(app)
        async with await db() as session:
            conn1 = await session.get_connection(db.engines['admin'])
            await self.models1.reset(conn1)
            conn1 = await session.get_connection(db.engines['front'])
            await self.models1.reset(conn1)
        return {
            'db': db,
        }

    async def aclose(self, db):
        db.close()

    @asynctest
    async def test_create_table(self, db):
        self.assertEqual(
            db.mappers.metadata['admin'].tables['PubTest'].c.keys(),
            ['id', 'state', 'title', 'title2'],
        )
        self.assertEqual(
            db.mappers.metadata['front'].tables['PubTest'].c.keys(),
            ['id', 'state', 'title', 'title2'],
        )
        self.assertEqual(
            db.mappers['admin']['PubTest'].table,
            db.mappers.metadata['admin'].tables['PubTest'],
        )
        self.assertEqual(
            db.mappers['front']['PubTest'].table,
            db.mappers.metadata['front'].tables['PubTest'],
        )

    @asynctest
    async def test_insert_item(self, db):
        mapper1 = db.mappers['admin']['PubTest']
        mapper2 = db.mappers['front']['PubTest']
        query1 = mapper1.query().order_by(mapper1.c['id'])
        query2 = mapper2.query().order_by(mapper2.c['id'])

        item1_1 = dict(self.item1, state='private')
        item1_2 = dict(self.item1, state='private', title=None, title2=None)

        item2_1 = dict(self.item2, state='private')
        item2_2 = dict(self.item2, state='private', title=None, title2=None)

        async with await db() as session:
            result = await query1.insert_item(
                session,
                dict(self.item1, id=None),
            )
            await session.commit()
            items = await query1.select_items(session)
            self.assertEqual(items, [item1_1])
            items = await query2.select_items(session)
            self.assertEqual(items, [item1_2])
            result = await query1.insert_item(
                session,
                dict(self.item2),
            )
            await session.commit()
            items = await query1.select_items(session)
            self.assertEqual(items, [item1_1, item2_1])
            items = await query2.select_items(session)
            self.assertEqual(items, [item1_2, item2_2])


    @asynctest
    async def test_delete_item(self, db):
        mapper1 = db.mappers['admin']['PubTest']
        mapper2 = db.mappers['front']['PubTest']
        query1 = mapper1.query().order_by(mapper1.c['id'])
        query2 = mapper2.query().order_by(mapper2.c['id'])

        item1_1 = dict(self.item1, state='private')
        item1_2 = dict(self.item1, state='private', title=None, title2=None)

        item2_1 = dict(self.item2, state='private')
        item2_2 = dict(self.item2, state='private', title=None, title2=None)

        async with await db() as session:
            result = await query1.insert_item(session, self.item1)
            result = await query1.insert_item(session, self.item2)
            await session.commit()
            await query1.delete_item(session, item1_1['id'])
            items = await query1.select_items(session)
            self.assertEqual(items, [item2_1])
            items = await query2.select_items(session)
            self.assertEqual(items, [item2_2])


    @asynctest
    async def test_publish(self, db):
        mapper1 = db.mappers['admin']['PubTest']
        mapper2 = db.mappers['front']['PubTest']
        query1 = mapper1.query().order_by(mapper1.c['id'])
        query2 = mapper2.query().order_by(mapper2.c['id'])

        item1_1 = dict(self.item1, state='public')
        item1_2 = dict(self.item1, state='public')

        item2_1 = dict(self.item2, state='private')
        item2_2 = dict(self.item2, state='private', title=None, title2=None)

        async with await db() as session:
            result = await query1.insert_item(session, self.item1)
            result = await query1.insert_item(session, self.item2)
            await session.commit()
            result = await query1.publish(session, item1_1['id'])
            items = await query1.select_items(session)
            self.assertEqual(items, [item1_1, item2_1])
            items = await query2.select_items(session)
            self.assertEqual(items, [item1_2, item2_2])

