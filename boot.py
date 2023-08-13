
print('\n\n')
print("--------------------- BOOT BOARD ---------------------")



#
# imports
#
import sys
import gc
import time

from events import Events
from config import CONFIG
import device
import logger



# 
# global constants
#
BOOT_MAX_SETUP_ATTEMPTS = 2
BOOT_COUNTER = 0
BOOT_WAIT_MS = CONFIG.get("BOOT_WAIT_MS")

MY_LOCATION = CONFIG.get("MY_LOCATION")
MY_MAC = CONFIG.get("MY_MAC")
MY_HOST = CONFIG.get("MY_HOST")
MY_STAGE = CONFIG.get("MY_STAGE")

MQTT_TOPIC_EVENTS = CONFIG.get("MQTT_TOPIC_EVENTS")

EVENTS_FILE = CONFIG.get("EVENTS_FILE")
EVENTS = Events(EVENTS_FILE, MY_STAGE, MY_LOCATION, MY_HOST, MQTT_TOPIC_EVENTS)



# 
# global variables
#
dev = None 
led = None
sensors = None
wdt = None



#
# boot sequence
# 
def boot_setup():
    global BOOT_COUNTER
    global BOOT_WAIT_MS
    global dev
    global led
    global sensors
    global wdt
    EVENTS.event("info", "boot setup running ...", BOOT_COUNTER)

    # loop to setup the board
    while True:
        BOOT_COUNTER += 1
        if BOOT_COUNTER > BOOT_MAX_SETUP_ATTEMPTS:
            wait_ms = BOOT_WAIT_MS * BOOT_COUNTER * BOOT_COUNTER
            EVENTS.event("error", "setup has failed MAX_SETUP_ATTEMPTS(%d) times. sleep %d milliseconds. hard reset..." % (BOOT_MAX_SETUP_ATTEMPTS, wait_ms))
            time.sleep_ms(wait_ms)
            EVENTS.hard_reset()

        try:
            wait_ms = BOOT_WAIT_MS
            time.sleep_ms(wait_ms)
            dev = device.Device(BOOT_COUNTER, CONFIG)
            led, sensors, wdt = dev.setup()
            wdt.feed()
            break

        except Exception as e:
            EVENTS.event("error", "setup failed", BOOT_COUNTER)
            sys.print_exception(e)
            wait_ms = BOOT_WAIT_MS * BOOT_COUNTER * BOOT_COUNTER
            EVENTS.event("error", "setup failed. sleep %d milliseconds. retry..." % wait_ms)
            time.sleep_ms(wait_ms)

    EVENTS.event("info", "boot setup done!", BOOT_COUNTER)



time.sleep_ms(BOOT_WAIT_MS)
try:
    # uncomment for testing the exception handling
    #from events import EventsException
    #raise EventsException("aaa")
    boot_setup()
except Exception as e:
    EVENTS.event("error", "Failed in boot_setup() function because of an Exception!", BOOT_COUNTER)
    sys.print_exception(e)
    time.sleep_ms(BOOT_WAIT_MS)
    EVENTS.soft_reset()
except:
    EVENTS.event("error", "Failed in boot_setup() function because of an *UNCATCHED* Exception!", BOOT_COUNTER)
    time.sleep_ms(BOOT_WAIT_MS)
    EVENTS.soft_reset()
