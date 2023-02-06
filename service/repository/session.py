from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

from utils.snippets import SingletonClass


class DBSessionHandler(SingletonClass):
    """
    SQLAlchemy session handler
    """
    def __init__(self, db_type: str, name: str, **kwargs) -> None:
        """
        Database setup
        :param db_type: database dialect
        :param name: database name or path
        :param kwargs: connection extras that may be needed
        """
        super().__init__()
        host = kwargs.get("host")
        port = kwargs.get("port")
        username = kwargs.get("username")
        password = kwargs.get("password")
        pool_size = kwargs.get("pool_size", 5)
        if db_type == "sqlite":
            uri = f"sqlite:///{name}"
            self.db_engine = create_engine(uri)
        elif host and port and username and password:
            uri = f"{db_type}://{username}:{password}@{host}:{port}/{name}"
            self.db_engine = create_engine(uri, pool_size=pool_size)
        else:
            raise AttributeError(
                f'{db_type} dialect needs username, password host and port'
            )

        self.Session = sessionmaker(bind=self.db_engine)

    @contextmanager
    def context_session(self):
        session = self.Session()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.expunge_all()
            session.close()

    def save(self, obj: object) -> None:
        with self.context_session() as session:
            session.add(obj)
