import time
import logger
from wifi import Wifi



# 
# global constants
#

SENSOR_PIN  = 2
LED_PIN     = 14

MY_HOST      = 'esp-sensor-wifi-scan'

SCAN_INTERVAL  = 5



#
# functions
#

def setup_board():
	print('\n\n')
	print('--------------------- SETUP BOARD ---------------------')
	time.sleep(1)
	logger.board_info()
	logger.disable_debug()


def setup_wifi():
	try:
		w = Wifi()
		w.set_hostname(MY_HOST)
	except OSError as ose:
		logger.print_error("WIFI Setup Failed!")
		raise

	return w



#
# program
#

def main():
	w = None
	m = None


	# loop to setup the board
	while True:
		try:
			setup_board()
			w = setup_wifi()
			break
		except OSError as ose:
			print("Setup failed:", ose)


	# loop for scanning
	while True:
		print('----------- SCANNING -----------')
		list = w.scan_ssids()
		for i in list:
			print(i)
		time.sleep(SCAN_INTERVAL)


main()
