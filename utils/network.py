from service.model.message import Message
from utils.snippets import SingletonClass


class Network(SingletonClass):
    """
    Class with messages on buffer
    """
    def __init__(self):
        super().__init__()
        self._buffer = []

    def getall(self) -> list:
        """
        Method to get all messages in buffer
        :return: messages in buffer
        """
        return self._buffer or None

    def publish(self, message: Message) -> None:
        self._buffer.append(message)
