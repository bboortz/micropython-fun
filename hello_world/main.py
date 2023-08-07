from events import Events
from config import CONFIG
from sensors import get_sensors
import neoled

import sys
import time
import ujson as json
import logger
from machine import Pin
from machine import WDT



# 
# global constants
#

MAX_SETUP_ATTEMPTS = 2
MAX_ERRORS = 10
MAX_COUNTER = sys.maxsize - 1000
COUNTER = 0
ERR_COUNTER = 0

EVENTS_FILE = CONFIG.get("EVENTS_FILE")

MY_LOCATION = CONFIG.get("MY_LOCATION")
MY_MAC = CONFIG.get("MY_MAC")
MY_HOST = CONFIG.get("MY_HOST")
MY_STAGE = CONFIG.get("MY_STAGE")

MQTT_BROKER = CONFIG.get("MQTT_BROKER")
MQTT_CLIENT_NAME = CONFIG.get("MQTT_CLIENT_NAME")
MQTT_TOPIC = CONFIG.get("MQTT_TOPIC")
MQTT_TOPIC_EVENTS = CONFIG.get("MQTT_TOPIC_EVENTS")

BOOT_WAIT_MS = CONFIG.get("BOOT_WAIT_MS")
HELLO_INTERVAL_MS  = CONFIG.get("HELLO_INTERVAL_MS")

EVENTS = Events(EVENTS_FILE, MY_STAGE, MY_LOCATION, MY_HOST, MQTT_TOPIC_EVENTS)



#
# functions
#

def setup_board():
    print('\n\n')
    print("--------------------- SETUP BOARD: %d ---------------------" % COUNTER)
    time.sleep_ms(1000)
    logger.board_info()
    print(CONFIG)
    time.sleep_ms(1000)
    logger.disable_debug()

    # setup pins
    led_pin = CONFIG.get("LED_PIN")
    led = Pin(led_pin, Pin.OUT)
    led = neoled.NeoLed(led, 1)
    sensors = get_sensors()

    return led, sensors


def measure(mqtt, counter, sensors, topic):
    global ERR_COUNTER

    try:
        t = time.localtime()
        datetime = "%4d-%02d-%02dT%02d:%02d:%02d.000Z" % (t[0], t[1], t[2], t[3], t[4], t[5])
        ticks_s = int(time.ticks_ms() / 1000)

        json_data = { 
            "stage": MY_STAGE, 
            "location": MY_LOCATION,
            "device": MY_HOST,
            "measure_count": counter, 
            "datetime": datetime,
            "ticks_s": ticks_s,
#            "vorlauf_temp": temp_vorlauf_res,
#            "ruecklauf_temp": temp_ruecklauf_res
        }

        for s in sensors:
            name = s.get("name")
            sensor = s.get("sensor")
            sensor_res = sensor.measure()
            sensor.init_next_measure()
            json_data.update({name: sensor_res})
            print("Temperature: %3.3f °C" % sensor_res)

        json_str = json.dumps(json_data)
        print(json_str)
        mqtt.publish(topic, json_str)
        # mqtt.publish(topic + "-temp", str(temp))
        # mqtt.publish(topic_begin + "-humi", str(humi))
    except Exception as e:
        EVENTS.event("error", "Measurement failed: %s" % getattr(e, 'message', repr(e)) )
        ERR_COUNTER += 1
        if ERR_COUNTER > MAX_ERRORS:
            EVENTS.event("error", "initiating soft reset because ERR_COUNTER is reaching MAX_ERRORS.")
            EVENTS.soft_reset()


#
# program
#

def main():
    global COUNTER
    global ERR_COUNTER
    global MAX_SETUP_ATTEMPTS
    global BOOT_WAIT_MS
    w = None
    m = None
    led = None
    voltpin = None
    wdt = None
    EVENTS.event("info", "initializing boot ...", COUNTER)

    # loop to setup the board
    while True:
        COUNTER += 1
        if COUNTER > MAX_SETUP_ATTEMPTS:
            wait_ms = BOOT_WAIT_MS * COUNTER * COUNTER
            EVENTS.event("error", "setup has failed MAX_SETUP_ATTEMPTS(%d) times. sleep %d milliseconds. hard reset..." % (MAX_SETUP_ATTEMPTS, wait_ms))
            time.sleep_ms(wait_ms)
            EVENTS.hard_reset()

        try:
            led, sensors = setup_board()
            # wdt = WDT(timeout = WDT_TIMEOUT)
            wdt = WDT()
            EVENTS.event("info", "WDT initiated", COUNTER)
            wdt.feed()
            break

        except Exception as e:
            EVENTS.event("error", "setup failed", COUNTER)
            sys.print_exception(e)
            wait_ms = BOOT_WAIT_MS * COUNTER * COUNTER
            EVENTS.event("error", "setup failed. sleep %d milliseconds. retry..." % wait_ms)
            time.sleep_ms(wait_ms)


    COUNTER = 0
    EVENTS.event("info", "setup done", COUNTER)
    led.color((2, 2, 2))
    time.sleep_ms(BOOT_WAIT_MS)
    led.color((0, 0, 0))
    wdt.feed()

    # loop for measuring and publishing data
    while True:
        if COUNTER > MAX_COUNTER:
            EVENTS.event("error", "initiating soft reset because COUNTER is reaching MAX_COUNTER.")
            EVENTS.soft_reset()

        print("----------- HELLO: %d -----------" % COUNTER)
        wdt.feed()
        led.color((2, 2, 2))
        time.sleep_ms(HELLO_INTERVAL_MS)
        led.color((0, 0, 0))
        COUNTER += 1
        wdt.feed()


while True:
    try:
        # uncomment for testing the exception handling
        #from events import EventsException
        #raise EventsException("aaa")
        main()
    except Exception as e:
        EVENTS.event("error", "Failed in main() function because of an Exception!", COUNTER)
        sys.print_exception(e)
        EVENTS.soft_reset()
    except:
        EVENTS.event("error", "Failed in main() function because of an *UNCATCHED* Exception!", COUNTER)
        EVENTS.soft_reset()

