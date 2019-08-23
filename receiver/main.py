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

SOUND_PIN   = 2
LED_PIN     = 14

MY_LOCATION  = 'house-floor0'
MY_MAC       = '10aea47b9791'
MY_HOST      = 'esp-recv-' + MY_LOCATION

#MQTT_BROKER       = "192.168.2.12"
MQTT_BROKER       = "192.168.43.163"
MQTT_CLIENT_NAME  = MY_HOST 
MQTT_TOPIC_ALIVE   = 'sensornet/' + MY_LOCATION + '/alive'

PUBLISH_INTERVAL  = 5

SOUND = None
SOUND = Pin(SOUND_PIN, Pin.OUT)



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
	SOUND = sound = Pin(SOUND_PIN, Pin.OUT)
	led = Pin(LED_PIN, Pin.OUT)

	return sound, led


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

def on_message(topic, msg):
	print((topic, msg))
	SOUND.value(1)
	time.sleep(0.5)
	SOUND.value(0)


def recv(mqtt):
	mqtt.subscribe("sensornet/house-floor0/alive", on_message)
	mqtt.wait_msg()



#
# program
#

def main():
	w = None
	m = None


	# loop to setup the board
	while True:
		try:
			sound, led = setup_board()
			w = setup_wifi()
			m = setup_mqtt()
			break
		except OSError as ose:
			print("Setup failed:", ose)


	# loop for measuring and publishing data
	while True:
		print('----------- NEXT CYCLE -----------')
		recv(m)
		time.sleep(PUBLISH_INTERVAL)

	# cleanup
	m.disconnect()
	w.disconnect()


while True:
	main()
