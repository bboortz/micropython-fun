import logger
import time
import network
import ubinascii
from umqtt.simple import MQTTClient



#
# class
#

class Mqtt:

	def __init__(self, client_name, server):
		self.__c = MQTTClient(client_name, server)
		self.__connected = False


	def is_connected(self):
		try:
			logger.print_cmd('Send MQTT ping')
			self.__c.ping()
			self.__connected = True
			logger.print_info('Connected from MQTT Broker')
		except:
			self.disconnect(False)
		return self.__connected


	def connect(self):
		logger.print_cmd('Connect to MQTT Broker')
		self.__c.connect()
		self.is_connected()


	def disconnect(self, force=False):
		if self.__connected or force:
			logger.print_cmd('Disconnected from MQTT Broker')
			self.__connected = False
			self.__c.disconnect()


	def publish(self, topic, msg):
		logger.print_cmd('Publish data vi MQTT')
		self.__c.publish(topic, msg)
