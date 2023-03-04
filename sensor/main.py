import time
import dht
from machine import Pin, ADC
import ujson as json
import logger
from wifi import Wifi
from mqtt import Mqtt
from secrets import WIFI_SSID, WIFI_PASS



# 
# global constants
#

ADC_VORLAUF_PIN = 34
ADC_RUECKLAUF_PIN = 35
SENSOR_VORLAUF_DHT22_PIN  = 0 # anderes 4
SENSOR_RUECKLAUF_DHT22_PIN  = 5 
LED_PIN     = 14

MY_LOCATION  = 'cellar-heating'
MY_MAC       = '10aea47b9790'
MY_HOST      = 'esp-sensor-' + MY_LOCATION

MQTT_BROKER       = "192.168.1.3"
MQTT_CLIENT_NAME  = MY_HOST 
MQTT_TOPIC_VORLAUF        = 'sensornet/' + MY_LOCATION + '/vorlauf'
MQTT_TOPIC_RUECKLAUF      = 'sensornet/' + MY_LOCATION + '/ruecklauf'

PUBLISH_INTERVAL  = 5



#
# functions
#

def setup_board():
    print('\n\n')
    print('--------------------- SETUP BOARD ---------------------')
    time.sleep(1)
    logger.board_info()
    logger.disable_debug()

    # setup pins
    dht_vorlauf = dht.DHT22(Pin(SENSOR_VORLAUF_DHT22_PIN))
    dht_ruecklauf = dht.DHT22(Pin(SENSOR_RUECKLAUF_DHT22_PIN))
    led = Pin(LED_PIN, Pin.OUT)
    voltpin_vorlauf = ADC(Pin(ADC_VORLAUF_PIN))
    voltpin_vorlauf.atten(ADC.ATTN_11DB)
    voltpin_ruecklauf = ADC(Pin(ADC_RUECKLAUF_PIN))
    voltpin_ruecklauf.atten(ADC.ATTN_11DB)

    return dht_vorlauf, dht_ruecklauf, led, voltpin_vorlauf, voltpin_ruecklauf


def setup_wifi():
    try:
        w = Wifi()
        w.set_hostname(MY_HOST)
        w.connect(WIFI_SSID, WIFI_PASS)
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


def measure_temp(mqtt, dht, topic_begin):
    try:
        dht.measure()
            
        temp = dht.temperature()
        #humi = dht.humidity()
        print("Temperature: %3.1f °C" % temp)
        #print("   Humidity: %3.2f %% RH" % humi)

        #json_data = {
        #    "location": MY_LOCATION,
        #    "temperature": temp,
        #    "humidity":humi 
        #}
        #json_str = json.dumps(json_data)
        mqtt.publish(topic_begin + "-temp", str(temp))
        # mqtt.publish(topic_begin + "-humi", str(humi))
    except OSError as ose:
        print("Meeasurement failed:", ose)
    #   raise


def measure_volt(mqtt, voltpin, topic_begin):
    try:
        voltpin_value = voltpin.read()
        volt = voltpin_value * 3.3 / 4095
                
        print("Volt: %f V" % volt)

        json_data = {
            "location": MY_LOCATION,
            "volt":volt
        }
        json_str = json.dumps(json_data)
        mqtt.publish(topic_begin + "-volt", str(volt))
    except OSError as ose:
        print("Meeasurement failed:", ose)
    #        raise



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
            dht_vorlauf, dht_ruecklauf, led, voltpin_vorlauf, voltpin_ruecklauf = setup_board()
            w = setup_wifi()
            m = setup_mqtt()
            break
        except OSError as ose:
            print("Setup failed:", ose)
    time.sleep(3)

    # loop for measuring and publishing data
#    while board_ready and w.is_connected() and m.is_connected():
    while True:
        print('----------- MEASURE AND PUBLISH -----------')
        measure_temp(m, dht_vorlauf, MQTT_TOPIC_VORLAUF)
        measure_temp(m, dht_ruecklauf, MQTT_TOPIC_RUECKLAUF)
        measure_volt(m, voltpin_vorlauf, MQTT_TOPIC_VORLAUF)
        measure_volt(m, voltpin_ruecklauf, MQTT_TOPIC_RUECKLAUF)
#        led.value(1)
#        time.sleep(0.5)
#        print('led 0')
#        led.value(0)
#        print('sleep')
        time.sleep(PUBLISH_INTERVAL)

    # cleanup
    m.disconnect()
    w.disconnect()


while True:
    main()


# testcases
# 
# during startup
# * wifi available / unavailable
# * mqtt available / unavailable
# * sensor available / unavailable
#
# during runtime
# * wifi available / unavailable
# * mqtt available / unavailable
# * sensor available / unavailable
