from service.model.message import Message
from service.repository.session import DBSessionHandler


class Repository:
    """
    Main class for repository pattern
    """
    def __init__(self, db_type: str, **kwargs) -> None:
        self._db = DBSessionHandler(db_type, **kwargs)
        Message.metadata.create_all(self._db.db_engine, checkfirst=True)

    def save(self, message):
        if isinstance(message, list):
            for m in message:
                self._db.save(m)
        else:
            self._db.save(message)
