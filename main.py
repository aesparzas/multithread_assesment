import sys

from logs.logging import Logging
from sensors.base_sensor import BaseSensor
from service.repository.repository import Repository
from utils.network import Network

if __name__ == '__main__':
    repository = Repository(db_type='sqlite', name='db.db')
    network = Network()
    sensors = [
        BaseSensor(f'Sensor {i}', 5, network, 0, 100) for i in range(5)
    ]
    logging = Logging(repository, network)
    for s in sensors:
        s.start()
    logging.start()

    try:
        while True:
            pass
    except KeyboardInterrupt as e:
        for s in sensors:
            s.is_running = False
        while sensors:
            for s in sensors:
                s.join(0.5)
                if not s.is_alive():
                    sensors.remove(s)
        while logging.is_alive():
            logging.join(0.5)
        sys.exit(e)
