import logging
import threading
from random import randint
from time import sleep

from service.model.message import Message
from utils.network import Network


class BaseSensor(threading.Thread):
    """
    Class to handle sensors publishing info in the network. Each sensor
    in a thread
    """
    def __init__(self, name: str, delay: int, network: Network, min_value: int,
                 max_value: int) -> None:
        """
        Initialization for each sensor
        :param name: name of the sensor
        :param delay: delay in time of each value the sensor reads
        :param network: network to temporary store the messages
        :param min_value: minimum of the sensor to read
        :param max_value: maximum of the sensor to read
        """
        super().__init__()
        self.name = name
        self.min_value = min_value
        self.max_value = max_value
        self._delay = delay
        self._network = network
        self.is_running = False

    def read(self) -> int:
        """
        Method to get the integer value of a sensor
        :return:
        integer between the minimum and maximum established
        """
        reading = randint(self.min_value, self.max_value)
        return reading

    def publish(self, message: Message) -> None:
        """
        Method to publish the reading of this sensor
        :param message: message to publish
        """
        self._network.publish(message)

    def run(self):
        """
        Threading process of the sensor
        """
        self.is_running = True
        try:
            while self.is_running:
                value = self.read()
                message = Message(sensor_name=self.name, value=value)
                logging.info(f"Message from {self.name}: {message}")
                self.publish(message)
                sleep(self._delay)
        finally:
            logging.debug(f"Stopped sensor: {self.name}")