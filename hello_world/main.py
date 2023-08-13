
print('\n\n')
print("--------------------- RUN PROGRAM ---------------------")



#
# imports
#
from events import Events
from config import CONFIG

import sys
import time
import ujson as json
import logger
from machine import Pin



# 
# global constants
#
MAX_SETUP_ATTEMPTS = 2
MAX_ERRORS = 10
MAX_COUNTER = sys.maxsize - 1000
COUNTER = 0
ERR_COUNTER = 0

MQTT_BROKER = CONFIG.get("MQTT_BROKER")
MQTT_CLIENT_NAME = CONFIG.get("MQTT_CLIENT_NAME")
MQTT_TOPIC = CONFIG.get("MQTT_TOPIC")

HELLO_INTERVAL_MS  = CONFIG.get("HELLO_INTERVAL_MS")



#
# functions
#
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
    EVENTS.event("info", "program setup runnig ...", COUNTER)

    # loop to setup the board
    while True:
        COUNTER += 1
        if COUNTER > MAX_SETUP_ATTEMPTS:
            wait_ms = BOOT_WAIT_MS * COUNTER * COUNTER
            EVENTS.event("error", "setup has failed MAX_SETUP_ATTEMPTS(%d) times. sleep %d milliseconds. hard reset..." % (MAX_SETUP_ATTEMPTS, wait_ms))
            time.sleep_ms(wait_ms)
            EVENTS.hard_reset()

        try:
            wdt.feed()
            break

        except Exception as e:
            EVENTS.event("error", "setup failed", COUNTER)
            sys.print_exception(e)
            wait_ms = BOOT_WAIT_MS * COUNTER * COUNTER
            EVENTS.event("error", "setup failed. sleep %d milliseconds. retry..." % wait_ms)
            time.sleep_ms(wait_ms)


    COUNTER = 0
    EVENTS.event("info", "program setup done", COUNTER)
    led.on()
    time.sleep_ms(BOOT_WAIT_MS)
    led.off()
    wdt.feed()
    EVENTS.event("info", "program setup really done", COUNTER)

    # loop for measuring and publishing data
    while True:
        if COUNTER > MAX_COUNTER:
            EVENTS.event("error", "initiating soft reset because COUNTER is reaching MAX_COUNTER.")
            EVENTS.soft_reset()

        print("----------- HELLO: %d -----------" % COUNTER)
        wdt.feed()
        led.on()
        time.sleep_ms(HELLO_INTERVAL_MS)

        wdt.feed()
        led.off()
        time.sleep_ms(HELLO_INTERVAL_MS)
        COUNTER += 1


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

