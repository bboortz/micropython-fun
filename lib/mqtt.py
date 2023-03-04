import logger
import time
import network
import ubinascii
#from umqtt.simple import MQTTClient
from umqtt.robust import MQTTClient



#
# class
#

class Mqtt:

	def __init__(self, client_name,server):
		self.__c = MQTTClient(client_id=client_name, server=server, keepalive=5)
		self.__connected = False


	def is_connected(self):
		try:
			logger.print_cmd('Send MQTT ping')
			self.__c.ping()
			self.__connected = True
			logger.print_info('Connected to MQTT Broker')
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
		logger.print_cmd('Publish data via MQTT topic: {}'.format(topic))
		self.__connected = False
		self.__c.publish(topic, msg)


	def subscribe(self, topic, message_func):
		logger.print_cmd('Subscribe data vi MQTT')
		self.__c.set_callback(message_func)
		self.__c.subscribe(topic)


	def wait_msg(self):
		try:
			while 1:
				self.__c.wait_msg()
		finally:
			self.__c.disconnect()
