import logging

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, scoped_session, sessionmaker

logger = logging.getLogger()


class ORMUnitOfWork:
    session_factory: sessionmaker
    session: Session

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
        _create_engine = create_engine(self._db_url, echo=True)
        return sessionmaker(bind=_create_engine)

    def __init__(self):
        super().__init__()
        self.session_factory = self._sessionmaker()
        self.session = None

    def __enter__(self):
        self.session: scoped_session = scoped_session(self.session_factory)
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
