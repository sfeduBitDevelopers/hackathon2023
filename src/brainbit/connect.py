import time

from neurosdk.scanner import Scanner
from neurosdk.sensor import SensorFamily

from src.brainbit.check_resistance import CheckResistance
from src.core.log_config import logger


class ScanDevices:
    def __init__(self):
        self.sensors = None
        self.scanner = Scanner([SensorFamily.LEBrainBit])

    def scan(self):
        # Scan for devices
        logger.info("Scanning for devices...")
        self.scanner.start()

        # Wait for 10 seconds
        time.sleep(5)

        logger.info("Scanning for devices... Done")
        # Stop scanning
        self.scanner.stop()
        self.sensors = self.scanner.sensors()
        logger.info(f"Found {len(self.sensors)} devices")
        if len(self.sensors) > 0:
            logger.info(f"Devices: {self.sensors}")
            return self.sensors
        else:
            return 'No devices'


if __name__ == '__main__':
    scan = ScanDevices()
    device = scan.scan()
    logger.info(device)