import gc
import time
import status_led
import logger
from machine import Pin
from watchdogtimer import WatchdogTimer
from sensors import get_sensors
import neoled


#
# class
#
class DeviceException(BaseException):
    pass


class Device:

    def __init__(self, counter, config):
        self.__counter = counter
        self.__config = config

    def setup(self):
        print('\n\n')
        print("--------------------- SETUP BOARD: %d ---------------------" % self.__counter)
        time.sleep_ms( self.__config.get("BOOT_WAIT_MS") )
        logger.print_info("** BOARD INFO **")
        logger.board_info()
        logger.print_info("** CONFIG **")
        print(self.__config)

        # logging
        logger.disable_debug()
        logger.print_info('Logging for hardware debugging disabled!')

        # configure garbage collector
        gc.enable()
        gc.collect()
        logger.print_info('GC configured!')

        # setup pins
        led = status_led.StatusLed(self.__config)
        led.on()
        logger.print_info('Status LED configured!')

        # sensors
        sensors = get_sensors(self.__config)
        logger.print_info('Sensors configured!')

        # setup watchdogtimer
        wdt = WatchdogTimer(self.__config.get("WDT_TIMEOUT_MS"))
        logger.print_info('Watchdog Timer configured!')

        led.off()
        return led, sensors, wdt

