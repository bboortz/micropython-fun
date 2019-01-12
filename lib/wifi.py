import logger
import time
import network
import ubinascii

# 
# global constants
#

# WIFI_SSID   = '404 Network unavailable IoT'
WIFI_SSID     = 'Stratum0'
# WIFI_PASS   = 'deinIOTdeviceGeht99mal'
WIFI_PASS     = 'stehtinderinfoecke'
MY_MAC        = '10aea47b9790'
MY_HOST       = 'esp32-webserver'




#
# class
#

class Wifi:

	def __init__(self):
		self.__nic = network.WLAN(network.STA_IF)


	def is_connected(self):
		logger.print_cmd('Test WIFI Connection')
		ret = self.__nic.isconnected()

		if not ret:
			logger.print_info('Wifi Disconnected!')
		else:
			logger.print_info('Wifi Connected!')

		return ret


	def connect(self, ssid, password):
		if not self.is_connected():
			logger.print_cmd('Connect to Wifi {}'.format(ssid))
			self.__nic.active(True)
			self.__nic.connect(ssid, password)
			while not self.__nic.isconnected():
				time.sleep_ms(500)


	def disconnect(self):
		logger.print_cmd('Disconnect from Wifi')
		self.__nic.disconnect()


	def info(self):
		if self.is_connected():
			print('Wifi ESSID:', self.__nic.config('essid'))
			print('Network config:', self.__nic.ifconfig())
			mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
			print('Mac: {}'.format(mac))


	def set_mac(self, mac):
		logger.print_cmd('Set MAC to {}'.format(mac))

		emac = mac.encode()
		bmac = ubinascii.unhexlify(emac)
		self.__nic.config(mac=bmac)


	def set_hostname(self, host):
		logger.print_cmd('Set Hostname to {}'.format(host))
		self.__nic.config(dhcp_hostname=host)
