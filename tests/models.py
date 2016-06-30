from sqlalchemy.schema import MetaData
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy import sql


class ModelsBase:
    async def reset(self, conn):
        for table in self.metadata.sorted_tables:
            try:
                await conn.execute(sql.ddl.DropTable(table))
            except Exception:
                pass
            await conn.execute(sql.ddl.CreateTable(table))


class Models1(ModelsBase):
    metadata = MetaData()
    test_table1 = Table('test_table1', metadata,
        Column('id', Integer, primary_key=True),
        Column('title', String(60), nullable=True),
        Column('title2', String(60), nullable=True),
    )


class Models2(ModelsBase):
    metadata = MetaData()
    test_table2 = Table('test_table2', metadata,
        Column('id', Integer, primary_key=True),
        Column('title', String(60), nullable=True),
        Column('title2', String(60), nullable=True),
    )


models1 = Models1()
models2 = Models2()


