import logging
from datetime import datetime

import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.decl_api import DeclarativeMeta

logger = logging.getLogger()


class ORMUnitOfWork:
    session_factory: orm.sessionmaker
    session: orm.Session

    USER_NAME: str = "surveys"
    USER_PASS: str = "notsecure"
    DB_NAME: str = "surveys"
    DB_SCHEMA: str = "analysis"
    DB_HOST: str = "pg-server"
    DB_PORT: int = 5432
    DRIVER: str = "psycopg"
    TYPE: str = "postgresql"

    @property
    def _db_url(self):
        return f"{self.TYPE}+{self.DRIVER}://{self.USER_NAME}:{self.USER_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    def _sessionmaker(self):
        _create_engine = sa.create_engine(self._db_url, echo=True)
        return orm.sessionmaker(bind=_create_engine)

    def __init__(self):
        super().__init__()
        self.session_factory = self._sessionmaker()
        self.session = None

    def __enter__(self):
        self.session: orm.scoped_session = orm.scoped_session(self.session_factory)
        return self.session

    def __exit__(self, exception_type, exception_value, traceback):
        self.session.close()

        if exception_type and issubclass(exception_type, SQLAlchemyError):
            logger.error(
                "ORM SQLAlchemy error. Type {}, Value {}".format(
                    exception_type, exception_value
                ),
                exc_info=traceback,
            )
            raise SQLAlchemyError(exception_type, exception_value, traceback)


class ORMBase(metaclass=DeclarativeMeta):
    __abstract__ = True

    registry = orm.registry(metadata=sa.MetaData(schema="analysis"))
    metadata = sa.MetaData(schema="analysis")

    __init__ = registry.constructor


class MVSurveysStatus(ORMBase):
    __tablename__ = "mview_surveys_loaded_at_status"

    loaded_at: orm.Mapped[datetime] = orm.mapped_column(primary_key=True)
    status: orm.Mapped[str] = orm.mapped_column(sa.String(15))
    count: orm.Mapped[int] = orm.mapped_column(sa.Integer)


def get_surveys_by_loaded_at():
    sql_model = sa.select(MVSurveysStatus).order_by(MVSurveysStatus.loaded_at)
    sql_text = sa.text(
        "SELECT * FROM analysis.mview_surveys_loaded_at_status ORDER BY loaded_at"
    )

    with ORMUnitOfWork() as db:
        result_model = db.execute(sql_model).all()
        result_text = db.execute(sql_text).all()

    count = 0
    print(
        "Seq. |",
        " ",
        " sa.select(Model)       |",
        " sa.text('select ...')",
        sep="\t",
    )
    while count < 20:
        print(
            f"  {count}  |",
            f"{result_model[count][0].loaded_at} => {result_model[count][0].status}",
            "|",
            f"{result_text[count].loaded_at} => {result_text[count].status}",
            sep="\t",
        )
        count += 1


if __name__ == "__main__":
    get_surveys_by_loaded_at()
