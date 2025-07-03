from datetime import datetime

from base import ORMBase
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column


class MVSurveysStatus(ORMBase):
    __tablename__ = "mview_surveys_loaded_at_status"

    loaded_at: Mapped[datetime] = mapped_column(primary_key=True)
    status: Mapped[str] = mapped_column(String(15))
    count: Mapped[int] = mapped_column(Integer)
