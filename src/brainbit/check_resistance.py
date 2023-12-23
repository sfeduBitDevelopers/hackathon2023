import concurrent.futures

from neurosdk.cmn_types import *
from time import sleep

from src.core.log_config import logger


class CheckResistance:
    def __init__(self, device, scanner):
        self.device = device
        self.scanner = scanner
        self.resistance = {"O1": [], "O2": [], "T3": [], "T4": []}

    def on_resist_received(self, sensor, data):
        logger.info(f"Resistance: {data}")
        self.resistance["O1"].append(data.O1)
        self.resistance["O2"].append(data.O2)
        self.resistance["T3"].append(data.T3)
        self.resistance["T4"].append(data.T4)

    def device_connection(self):
        return self.scanner.create_sensor(self.device)

    def check_resistance(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(self.device_connection)
            sensor = future.result()
            logger.info("Device connected")

        logger.info("Checking resistance...")
        if sensor.is_supported_feature(SensorFeature.Resist):
            sensor.resistDataReceived = self.on_resist_received

        if sensor.is_supported_command(SensorCommand.StartResist):
            sensor.exec_command(SensorCommand.StartResist)
            logger.info("Start resist")
            sleep(5)
            sensor.exec_command(SensorCommand.StopResist)
            logger.info("Stop resist")

            logger.info(f"Resistance: {self.resistance}")

            del sensor
