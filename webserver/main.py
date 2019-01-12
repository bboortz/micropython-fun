import time
import logger
from wifi import Wifi
from mqtt import Mqtt
from secrets import WIFI_SSID, WIFI_PASS



# 
# global constants
#

MY_NAME   = 'esp32-webserver'
MY_MAC    = '10aea47b9790'
MY_HOST   = 'esp32-webserver'
MY_PORT   = 80

SERVER_ADDRESS     = ('0.0.0.0', MY_PORT)
REQUEST_QUEUE_SIZE = 1
TIMEOUT            = 3000				# in milliseconds



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
		w.connect(WIFI_SSID, WIFI_PASS)
		w.info()
	except OSError as ose:
		logger.print_error("WIFI Setup Failed!")
		raise

	return w


def web_page():
	json_data = {
		"status": {
			"healthy": True,
			"connected": True
		},
		"data": {
			"temperature": 20,
			"humidity": 10
		}
	}
	return json_data


def run_webserver():
	logger.print_cmd('Starting Webserver')
	import socket as socket
	import ujson as json

	s = socket.socket()
	s.settimeout(TIMEOUT)
	s.bind(SERVER_ADDRESS)
	s.listen(REQUEST_QUEUE_SIZE)

	logger.print_info('Serving HTTP on port {port} ...'.format(port=MY_PORT))

	while True:
		conn, addr = s.accept()
		request = conn.recv(1024)
		request = str(request)
		logger.print_info('%s - %s' % (addr[0], request))
		json_str = json.dumps(web_page())
		response = json_str + '\r\n'
		conn.send(response)
		conn.close()



#
# program
#

setup_board()
w = setup_wifi()
run_webserver()

