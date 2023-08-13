
print('\n\n')
print("--------------------- RUN PROGRAM ---------------------")



#
# import
# 
from events import Events
from config import CONFIG
from secrets import SECRETS
import temp

import sys
import time
import ujson as json
import logger
from wifi import Wifi
from wifi import WifiException
from mqtt import Mqtt



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

PUBLISH_INTERVAL_MS  = CONFIG.get("PUBLISH_INTERVAL_MS")




#
# functions
#
def setup_wifi(wdt):
    try:
        w = Wifi(wdt)
        w.activate()
        w.set_hostname(MY_HOST)
        w.set_mac(MY_MAC)
        w.connect(SECRETS.get("WIFI_SSID"), SECRETS.get("WIFI_PASS"))
        w.info()
    except Exception as e:
        EVENTS.event("error", "WIFI Setup Failed: %s" % getattr(e, 'message', repr(e)) )
        raise(e)
    except WifiException as be:
        EVENTS.event("error", "WIFI Setup Failed: %s. Deactivating interface." % getattr(be, 'message', repr(be)) )
        sys.print_exception(be)
        w.deactivate()
        raise(be)

    return w


def setup_mqtt():
    try:
        m = Mqtt(MQTT_CLIENT_NAME, MQTT_BROKER)
        m.connect()
    except Exception as e:
        EVENTS.event("error", "MQTT Setup Failed: %s" % getattr(e, 'message', repr(e)) )
        raise(e)

    return m


def setup_ntptime():
    import ntptime

    logger.print_info("Local time before synchronization：%s" %str(time.localtime()))
    ntptime.settime()
    logger.print_info("Local time after synchronization：%s" %str(time.localtime()))


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
            wait_ms = BOOT_WAIT_MS
            time.sleep_ms(wait_ms)
            w = setup_wifi(wdt)
            wdt.feed()
            m = setup_mqtt()
            wdt.feed()
            setup_ntptime()
            wdt.feed()
            break

        except WifiException as be:
            wait_ms = BOOT_WAIT_MS * COUNTER * COUNTER
            EVENTS.event("error", "setup failed. sleep %d milliseconds. retry..." % wait_ms)
            time.sleep_ms(wait_ms)
        except Exception as e:
            EVENTS.event("error", "setup failed", COUNTER)
            sys.print_exception(e)
            wait_ms = BOOT_WAIT_MS * COUNTER * COUNTER
            EVENTS.event("error", "setup failed. sleep %d milliseconds. retry..." % wait_ms)
            time.sleep_ms(wait_ms)


    COUNTER = 0
    EVENTS.set_mqtt(m, COUNTER)
    EVENTS.event("info", "program setup done", COUNTER)
    led.on()
    time.sleep_ms(BOOT_WAIT_MS)
    led.off()
    wdt.feed()

    # loop for measuring and publishing data
    while True:
        if COUNTER > MAX_COUNTER:
            EVENTS.event("error", "initiating soft reset because COUNTER is reaching MAX_COUNTER.")
            EVENTS.soft_reset()

        print("----------- MEASURE AND PUBLISH: %d -----------" % COUNTER)
        led.on()

        if len(sensors) == 0:
            logger.print_info("no sensors configured.")
        else:
            measure(m, COUNTER, sensors, MQTT_TOPIC)

        led.off()
        COUNTER += 1
        wdt.feed()
        time.sleep_ms(PUBLISH_INTERVAL_MS)
        wdt.feed()

    # cleanup
    m.disconnect()
    w.disconnect()


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

