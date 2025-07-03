from sqlalchemy import MetaData
from sqlalchemy.orm import registry
from sqlalchemy.orm.decl_api import DeclarativeMeta

metadata_obj = MetaData(schema="analysis")


class ORMBase(metaclass=DeclarativeMeta):
    __abstract__ = True

    registry = registry(metadata=metadata_obj)
    metadata = metadata_obj

    __init__ = registry.constructor
