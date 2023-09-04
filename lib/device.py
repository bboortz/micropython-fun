import gc
import time
import status_led
import button
import logger
import machine
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
        self.status_led = None
        self.boot_button = None
        self.sensors = None
        self.wdt = None

    def reset_cause_str(self, cause):
        switch={
            machine.DEEPSLEEP_RESET:'deepsleep reset',
            machine.HARD_RESET:'hard reset',
            machine.SOFT_RESET:'soft reset',
            machine.PWRON_RESET:'poweron reset',
            machine.WDT_RESET:'watchdog timer reset'
        }
        return switch.get(cause,"Unknown Reset Cause!")

    def deepsleep(self, deepsleep_ms):
        if deepsleep_ms == None  or  deepsleep_ms <= 0:
            return

        logger.print_info("Deepsleep for %d seconds ..." % deepsleep_ms)
        machine.deepsleep(deepsleep_ms)

    def setup(self, callback_boot_button=button.callback_button):
        print('\n\n')
        print("--------------------- SETUP BOARD: %d ---------------------" % self.__counter)
        time.sleep_ms( self.__config.get("BOOT_WAIT_MS") )
        logger.print_info("** BOARD INFO **")
        logger.board_info()
        print("reset cause: %s" % self.reset_cause_str( machine.reset_cause() ))
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
        self.status_led = status_led.StatusLed(self.__config)
        self.status_led.on()
        logger.print_info('Status LED configured!')

        boot_button_no = self.__config.get("BOOT_BUTTON")
        self.boot_button = button.Button(boot_button_no)
        self.boot_button.irq(callback=callback_boot_button)
        logger.print_info('Boot Button configured!')

        # sensors
        self.sensors = get_sensors(self.__config)
        logger.print_info('Sensors configured!')

        # setup watchdogtimer
        self.wdt = WatchdogTimer(self.__config.get("WDT_TIMEOUT_MS"))
        logger.print_info('Watchdog Timer configured!')

        self.status_led.off()

