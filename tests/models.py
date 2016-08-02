from sqlalchemy.schema import MetaData
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Date
from sqlalchemy import Table
from sqlalchemy import sql
from sqlalchemy.ext.declarative import declarative_base




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
    Base = declarative_base(metadata=metadata)

    class Test(Base):
        __tablename__ = 'test_table1'
        id =  Column(Integer, primary_key=True)
        title = Column(String(60), nullable=True)
        title2 = Column(String(60), nullable=True)
        date = Column(Date, nullable=True)

    test_table1 = Test.__table__


class Models2(ModelsBase):
    metadata = MetaData()
    Base = declarative_base(metadata=metadata)

    class Test(Base):
        __tablename__ = 'test_table2'
        id =  Column(Integer, primary_key=True)
        title = Column(String(60), nullable=True)
        title2 = Column(String(60), nullable=True)

    test_table2 = Test.__table__


models1 = Models1()
models2 = Models2()

metadata = {
    'db1': models1.metadata,
    'db2': models2.metadata,
}

