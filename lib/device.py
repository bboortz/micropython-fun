import time
import logger
from machine import Pin
from watchdogtimer import WatchdogTimer
from sensors import get_sensors
import neoled


#
# functions
#
def setup_device(counter, config):
    print('\n\n')
    print("--------------------- SETUP BOARD: %d ---------------------" % counter)
    time.sleep_ms(1000)
    logger.board_info()
    print("*CONFIG*")
    print(config)
    logger.disable_debug()

    # setup pins
    led_pin = config.get("LED_PIN")
    led = Pin(led_pin, Pin.OUT)
    led = neoled.NeoLed(led, 1)
    sensors = get_sensors()

    # setup watchdogtimer
    wdt = WatchdogTimer(config.get("WDT_TIMEOUT_MS"))

    return led, sensors, wdt

