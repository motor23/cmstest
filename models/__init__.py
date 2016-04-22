from sqlalchemy.schema import MetaData
from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    String,
    Text,
    Enum,
    Boolean,
    ForeignKey,
)
from sqlalchemy.ext.declarative import declarative_base
from iktomi.db.sqla.declarative import AutoTableNameMeta, TableArgsMeta


metadata = MetaData()

TABLE_ARGS = {
    'mysql_engine': 'InnoDB',
    'mysql_default charset': 'utf8',
}

class ModelsMeta(AutoTableNameMeta, TableArgsMeta(TABLE_ARGS)): pass

Base = declarative_base(
    metadata=metadata,
    name='Base',
    metaclass=ModelsMeta,
)


class Tags(Base):

    id = Column(Integer, primary_key=True)
    title = Column(String(500), default='')
