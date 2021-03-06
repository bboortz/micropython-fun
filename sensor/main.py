import time
import dht
from machine import Pin
import ujson as json
import logger
from wifi import Wifi
from mqtt import Mqtt
from secrets import WIFI_SSID, WIFI_PASS



# 
# global constants
#

SENSOR_PIN  = 2
LED_PIN     = 14

MY_LOCATION  = 'house-floor0'
MY_MAC       = '10aea47b9790'
MY_HOST      = 'esp-sensor-' + MY_LOCATION

#MQTT_BROKER       = "192.168.2.12"
MQTT_BROKER       = "192.168.43.163"
MQTT_CLIENT_NAME  = MY_HOST 
MQTT_TOPIC_TEMP   = 'sensornet/' + MY_LOCATION + '/temp'
MQTT_TOPIC_HUMI   = 'sensornet/' + MY_LOCATION + '/humi'

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
	sensor = dht.DHT11(Pin(SENSOR_PIN))
	led = Pin(LED_PIN, Pin.OUT)

	return sensor, led


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


def measure(mqtt, dht):
#	try:
	dht.measure()
			
	temp = dht.temperature()
	humi = dht.humidity()
	print("Temperature: %3.1f °C" % temp)
	print("   Humidity: %3.2f %% RH" % humi)

	json_data = {
		"location": "lala",
		"temperature": temp,
		"humidity":humi 
	}
	json_str = json.dumps(json_data)
	mqtt.publish(MQTT_TOPIC_TEMP, str(temp))
	mqtt.publish(MQTT_TOPIC_HUMI, str(humi))
#	except OSError as ose:
#		print("Meeasurement failed:", ose)
#		raise



#
# program
#

def main():
	w = None
	m = None


	# loop to setup the board
	while True:
		try:
			sensor, led = setup_board()
			w = setup_wifi()
			m = setup_mqtt()
			break
		except OSError as ose:
			print("Setup failed:", ose)


	# loop for measuring and publishing data
#	while board_ready and w.is_connected() and m.is_connected():
	while True:
		print('----------- MEASURE AND PUBLISH -----------')
#		led.value(1)
#		time.sleep(0.5)
		measure(m, sensor)
#		print('led 0')
#		led.value(0)
#		print('sleep')
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
