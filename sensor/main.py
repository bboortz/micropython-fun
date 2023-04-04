from secrets import SECRETS
from config import CONFIG
from sensors import get_sensors
import temp
import neoled

import time
import ujson as json
import logger
from wifi import Wifi
from mqtt import Mqtt
from machine import Pin

if CONFIG.get("ADC_SENSOR"):
    from machine import ADC



# 
# global constants
#

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
        w.connect(SECRETS.get("WIFI_SSID"), SECRETS.get("WIFI_PASS"))
        w.info()
    except OSError as ose:
        logger.print_error("WIFI Setup Failed!")
        raise

    return w


def setup_mqtt():
    try:
        m = Mqtt(MQTT_CLIENT_NAME, MQTT_BROKER)
        m.connect()
    except OSError as ose:
        logger.print_error("MQTT Setup Failed!")
        raise

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

    led.color((2, 2, 2))
    time.sleep_ms(BOOT_WAIT_MS)
    led.color((0, 0, 0))

    # loop for measuring and publishing data
#    while board_ready and w.is_connected() and m.is_connected():
    counter = 0
    while True:
        print('----------- MEASURE AND PUBLISH -----------')
        led.color((2, 2, 2))
        measure(m, counter, sensors, MQTT_TOPIC)
        led.color((0, 0, 0))
        counter += 1
        time.sleep_ms(PUBLISH_INTERVAL_MS)

    # cleanup
    m.disconnect()
    w.disconnect()


while True:
    main()

