import logging
import threading

from service.repository.repository import Repository
from utils.network import Network


class Logging(threading.Thread):
    def __init__(self, repository: Repository, network: Network):
        super().__init__()
        self.repository: Repository = repository
        self.network: Network = network

    def run(self) -> None:
        while True:
            # You must save data present on network here, keep on mind that
            # network could have at maximum 5 messages
            # at the time.
            message = self.network.getall()
            logging.info(f"Consumer got message: {message}")
            self.repository.save(message)