import time
from machine import Pin
import logger
from wifi import Wifi
from mqtt import Mqtt
from secrets import WIFI_SSID, WIFI_PASS



# 
# global constants
#

LED_STATUS_PIN     = 12

BUTTON_A_PIN       = 27
BUTTON_B_PIN       = 14
BUTTON_LEFT_PIN    = 26
BUTTON_RIGHT_PIN   = 33
BUTTON_UP_PIN      = 25
BUTTON_DOWN_PIN    = 32

MY_NAME           = 'game-controller'
MY_MAC            = '10aea47b9790'
MY_HOST           = 'esp-sensor-' + MY_NAME 

MQTT_BROKER       = "192.168.2.12"
MQTT_CLIENT_NAME  = MY_HOST 
MQTT_TOPIC        = 'game/' + MY_NAME + '/control'



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
	ledStatus  = Pin(LED_STATUS_PIN, Pin.OUT)
	buttonA    = Pin(BUTTON_A_PIN,     Pin.IN, Pin.PULL_UP)
	buttonB    = Pin(BUTTON_B_PIN,     Pin.IN, Pin.PULL_UP)
	buttonL    = Pin(BUTTON_LEFT_PIN,  Pin.IN, Pin.PULL_UP)
	buttonR    = Pin(BUTTON_RIGHT_PIN, Pin.IN, Pin.PULL_UP)
	buttonU    = Pin(BUTTON_UP_PIN,    Pin.IN, Pin.PULL_UP)
	buttonD    = Pin(BUTTON_DOWN_PIN,  Pin.IN, Pin.PULL_UP)
	ledStatus.value(0)

	return ledStatus, buttonA, buttonB, buttonL, buttonR, buttonU, buttonD


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


def check_button(mqtt, button, buttonName, pressed):
	m = button.value()

	if not m  and  not pressed[buttonName]:
		pressed[buttonName] = True
		msg = buttonName + "-press"
		mqtt.publish(MQTT_TOPIC, msg)
	elif m  and  pressed[buttonName]:
		pressed[buttonName] = False
		msg = buttonName + "-release"
		mqtt.publish(MQTT_TOPIC, msg)


def measure(mqtt, pressed, buttonA, buttonB, buttonL, buttonR, buttonU, buttonD):
	msg = 0
	mA = buttonA.value()
	mB = buttonB.value()
	mL = buttonL.value()
	mR = buttonR.value()
	mU = buttonU.value()
	mD = buttonD.value()

	print(mA, mB, mL, mR, mU, mD)

	check_button(mqtt, buttonA, 'A', pressed)
	check_button(mqtt, buttonB, 'B', pressed)
	check_button(mqtt, buttonL, 'L', pressed)
	check_button(mqtt, buttonR, 'R', pressed)
	check_button(mqtt, buttonU, 'U', pressed)
	check_button(mqtt, buttonD, 'D', pressed)



#
# program
#

def main():
	w = None
	m = None

	pressed =	{
		"A": False,
		"B": False,
		"L": False,
		"R": False,
		"U": False,
		"D": False,
	}


	# loop to setup the board
	while True:
		try:
			led, buttonA, buttonB, buttonL, buttonR, buttonU, buttonD = setup_board()
			w = setup_wifi()
			m = setup_mqtt()
			led.value(1)
			break
		except OSError as ose:
			print("Setup failed:", ose)

	led.value(1)

	# loop for the controller
	while True:
		measure(m, pressed, buttonA, buttonB, buttonL, buttonR, buttonU, buttonD)
		time.sleep(0.01)

	# cleanup
	m.disconnect()
	w.disconnect()


main()
