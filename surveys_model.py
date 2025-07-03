from datetime import datetime

from sqlalchemy import Integer, MetaData, String
from sqlalchemy.orm import Mapped, mapped_column, registry
from sqlalchemy.orm.decl_api import DeclarativeMeta

metadata_obj = MetaData(schema="analysis")


class ORMBase(metaclass=DeclarativeMeta):
    __abstract__ = True

    registry = registry(metadata=metadata_obj)
    metadata = metadata_obj

    __init__ = registry.constructor


class MVSurveysStatus(ORMBase):
    __tablename__ = "mview_surveys_loaded_at_status"

    loaded_at: Mapped[datetime] = mapped_column(primary_key=True)
    status: Mapped[str] = mapped_column(String(15))
    count: Mapped[int] = mapped_column(Integer)
