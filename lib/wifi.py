import logger
import time
import network
import ubinascii

# 
# global constants
#



#
# class
#

class Wifi:

	def __init__(self):
		self.__nic = network.WLAN(network.STA_IF)
		self.__nic.active(True)
		logger.print_info('NIC active: {}'.format(self.nic.active()))


	def is_connected(self):
		logger.print_cmd('Test WIFI Connection')
		ret = self.__nic.isconnected()

		if not ret:
			logger.print_info('Wifi Disconnected!')
		else:
			logger.print_info('Wifi Connected!')

		return ret


	def connect(self, ssid, password):
		print(self.__nic.status())
		if not self.is_connected():
			logger.print_cmd('Connect to Wifi {}'.format(ssid))
			self.__nic.connect(ssid, password)
			while not self.__nic.isconnected():
				time.sleep_ms(500)
				logger.print_wait()
				#print(self.__nic.ifconfig())



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

	def scan_ssids(self):
		return self.__nic.scan()
