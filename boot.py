
print('\n\n')
print("--------------------- BOOT BOARD ---------------------")



#
# imports
#
import sys
import time
import uasyncio as asyncio

from events import Events
from config import CONFIG
from secrets import SECRETS
from wifi import Wifi
from wifi import WifiException
from mqtt import Mqtt
import device
import logger
from tasks import Tasks
from program_state import ProgramState



# 
# global constants
#
LIB_VERSION = 2

# TODO: here or in lib/program_state.py
BOOT_MAX_SETUP_ATTEMPTS = 2
BOOT_COUNTER = 0
BOOT_WAIT_MS = CONFIG.get("BOOT_WAIT_MS")

MY_LOCATION = CONFIG.get("MY_LOCATION")
MY_MAC = CONFIG.get("MY_MAC")
MY_HOST = CONFIG.get("MY_HOST")
MY_STAGE = CONFIG.get("MY_STAGE")

MQTT_TOPIC_STATES = CONFIG.get("MQTT_TOPIC_STATES")
MQTT_TOPIC_EVENTS = CONFIG.get("MQTT_TOPIC_EVENTS")
MQTT_BROKER = CONFIG.get("MQTT_BROKER")
MQTT_CLIENT_NAME = CONFIG.get("MQTT_CLIENT_NAME")

EVENTS_FILE = CONFIG.get("EVENTS_FILE")
EVENTS = Events(EVENTS_FILE, MY_STAGE, MY_LOCATION, MY_HOST, MQTT_TOPIC_EVENTS)



# 
# global variables
#
program_state = None
tasks = None



#
# functions
# 
def setup_wifi(wdt):
    global program_state
    try:
        wifi_ssid = SECRETS.get("WIFI_SSID")
        wifi_pass = SECRETS.get("WIFI_PASS")
        program_state.wifi = Wifi(wdt)
        program_state.wifi.do_connect(MY_HOST, MY_MAC, wifi_ssid, wifi_pass)
    except Exception as e:
        EVENTS.event("error", "WIFI Setup Failed: %s" % getattr(e, 'message', repr(e)) )
        raise(e)
    except WifiException as be:
        EVENTS.event("error", "WIFI Setup Failed: %s. Deactivating interface." % getattr(be, 'message', repr(be)) )
        sys.print_exception(be)
        program_state.wifi.deactivate()
        raise(be)


def setup_mqtt():
    try:
        program_state.mqtt = Mqtt(MQTT_CLIENT_NAME, MQTT_BROKER)
        program_state.mqtt.connect()
        EVENTS.set_mqtt(program_state.mqtt, program_state.counter)
    except Exception as e:
        EVENTS.event("error", "MQTT Setup Failed: %s" % getattr(e, 'message', repr(e)) )
        raise(e)


def setup_ntptime():
    import ntptime

    logger.print_info("Local time before synchronization：%s" %str(time.localtime()))
    ntptime.settime()
    logger.print_info("Local time after synchronization：%s" %str(time.localtime()))


def callback_stop(p):
    print('#### pin change', p)
    # tasks.cancel_all_tasks()
    program_state.set_state_stopped()



#
# tasks
#
async def control_task():
    while True:
        if program_state.is_stopped():
            EVENTS.event("info", "WDT from control_task", program_state.counter)
            program_state.wdt.feed()
        await asyncio.sleep_ms(5000)


async def setup_task():
    EVENTS.event("info", "program setup runnig ...", program_state.counter)

    while True:
        program_state.wdt.feed()
        wait_ms = BOOT_WAIT_MS
        await asyncio.sleep_ms(wait_ms)
        program_state.wdt.feed()

        if program_state.is_stopped():
            EVENTS.event("info", "task setup_task stopped!")
            break
        if program_state.is_setup_done():
            continue

        program_state.setup_counter += 1
        if program_state.setup_counter > program_state.max_setup_attempts:
            wait_ms = BOOT_WAIT_MS * program_state.setup_counter * program_state.setup_counter
            EVENTS.event("error", "setup has failed program_state.max_setup_attempts(%d) times. sleep %d milliseconds. hard reset..." % (program_state.max_setup_attempts, wait_ms))
            await asyncio.sleep_ms(wait_ms)
            EVENTS.hard_reset()

        try:
            program_state.led.on()
            setup_wifi(program_state.wdt)
            program_state.wdt.feed()
            setup_mqtt()
            program_state.wdt.feed()
            setup_ntptime()
            program_state.wdt.feed()
            program_state.led.off()
            program_state.wdt.feed()
            program_state.set_state_setup_done()
            continue

        except WifiException as be:
            wait_ms = BOOT_WAIT_MS * program_state.counter * program_state.counter
            EVENTS.event("error", "setup failed. sleep %d milliseconds. retry..." % wait_ms)
            await asyncio.sleep_ms(wait_ms)
        except Exception as e:
            EVENTS.event("error", "setup failed", program_state.counter)
            sys.print_exception(e)
            wait_ms = BOOT_WAIT_MS * program_state.counter * program_state.counter
            EVENTS.event("error", "setup failed. sleep %d milliseconds. retry..." % wait_ms)
            await asyncio.sleep_ms(wait_ms)



#
# boot sequence
# 
async def boot_setup():
    global BOOT_COUNTER
    global BOOT_WAIT_MS
    global program_state
    global tasks
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
            dev.setup(callback_boot_button=callback_stop)
            program_state = ProgramState(MY_STAGE, MY_LOCATION, MY_HOST, dev, MQTT_TOPIC_STATES)
            program_state.wdt.feed()
            tasks = Tasks()
            tasks.create_task("setup_task", setup_task())
            tasks.create_task("control_task", control_task())

            while not program_state.is_setup_done():
                await asyncio.sleep_ms(wait_ms)
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
    asyncio.run(boot_setup())
except Exception as e:
    EVENTS.event("error", "Failed in boot_setup() function because of an Exception!", BOOT_COUNTER)
    sys.print_exception(e)
    time.sleep_ms(BOOT_WAIT_MS)
    EVENTS.soft_reset()
except:
    EVENTS.event("error", "Failed in boot_setup() function because of an *UNCATCHED* Exception!", BOOT_COUNTER)
    time.sleep_ms(BOOT_WAIT_MS)
    EVENTS.soft_reset()
