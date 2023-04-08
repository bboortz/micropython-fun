from secrets import SECRETS
from config import CONFIG
from sensors import get_sensors
import temp
import neoled

import sys
import time
import ujson as json
import logger
from wifi import Wifi
from mqtt import Mqtt
from machine import Pin
from machine import soft_reset

if CONFIG.get("ADC_SENSOR"):
    from machine import ADC



# 
# global constants
#

MAX_COUNTER = sys.maxsize - 1000

MY_LOCATION = CONFIG.get("MY_LOCATION")
MY_MAC = CONFIG.get("MY_MAC")
MY_HOST = CONFIG.get("MY_HOST")
MY_STAGE = CONFIG.get("MY_STAGE")

MQTT_BROKER = CONFIG.get("MQTT_BROKER")
MQTT_CLIENT_NAME = CONFIG.get("MQTT_CLIENT_NAME")
MQTT_TOPIC = CONFIG.get("MQTT_TOPIC")

BOOT_WAIT_MS = CONFIG.get("BOOT_WAIT_MS")
PUBLISH_INTERVAL_MS  = CONFIG.get("PUBLISH_INTERVAL_MS")



#
# functions
#

def setup_board():
    print('\n\n')
    print('--------------------- SETUP BOARD ---------------------')
    time.sleep_ms(1000)
    logger.board_info()
    logger.disable_debug()
    measurement_interval_ms = CONFIG.get("MEASUREMENT_INTERVAL_MS")

    # setup pins
    led_pin = CONFIG.get("LED_PIN")
    led = Pin(led_pin, Pin.OUT)
    led = neoled.NeoLed(led, 1)
    sensors = get_sensors()

    return led, sensors


def setup_wifi():
    try:
        w = Wifi()
        w.set_hostname(MY_HOST)
        w.set_mac(MY_MAC)
        w.connect(SECRETS.get("WIFI_SSID"), SECRETS.get("WIFI_PASS"))
        w.info()
    except Exception as e:
        logger.print_error("WIFI Setup Failed!")
        print(e)
        raise()

    return w


def setup_mqtt():
    try:
        m = Mqtt(MQTT_CLIENT_NAME, MQTT_BROKER)
        m.connect()
    except Exception as e:
        logger.print_error("MQTT Setup Failed!")
        print(e)
        raise()

    return m


def measure(mqtt, counter, sensors, topic):
    try:
        ticks_s = time.time()
        json_data = { 
            "stage": MY_STAGE, 
            "location": MY_LOCATION,
            "device": MY_HOST,
            "measure_count": counter, 
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

        # counter = 0
        json_str = json.dumps(json_data)
        print(json_str)
        mqtt.publish(topic, json_str)
        # mqtt.publish(topic + "-temp", str(temp))
        # mqtt.publish(topic_begin + "-humi", str(humi))
    except Exception as e:
        logger.print_error("Measurement failed!")
        print(e)


#
# program
#

def main():
    w = None
    m = None
    led = None
    voltpin = None

    # loop to setup the board
    while True:
        try:
            led, sensors = setup_board()
            w = setup_wifi()
            m = setup_mqtt()
            break
        except Exception as e:
            logger.print_error("Setup failed!")
            print(e)
            raise()

    led.color((2, 2, 2))
    time.sleep_ms(BOOT_WAIT_MS)
    led.color((0, 0, 0))

    # loop for measuring and publishing data
#    while board_ready and w.is_connected() and m.is_connected():
    counter = 0
    while True:
        if counter > MAX_COUNTER:
            logger.print_info("initiazing soft reset because counter is reaching MAX_COUNTER")
            soft_reset()

        print("----------- MEASURE AND PUBLISH: %d -----------" % counter)
        led.color((2, 2, 2))

        if len(sensors) == 0:
            logger.print_info("no sensors configured.")
        else:
            measure(m, counter, sensors, MQTT_TOPIC)

        led.color((0, 0, 0))
        counter += 1
        time.sleep_ms(PUBLISH_INTERVAL_MS)

    # cleanup
    m.disconnect()
    w.disconnect()


while True:
    try:
        main()
    except Exception as e:
        logger.print_error("Failed in main() function!")
        print(e)
        soft_reset()

