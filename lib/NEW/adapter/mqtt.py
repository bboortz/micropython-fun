import time


from core.logger import Logger
from core.config import Config
try:
    from contrib.umqtt.robust import MQTTClient as MqttClient
except:
    from paho.mqtt.client import Client as MqttClient
from domain.messaging import Messaging



#
# class
#
class Mqtt(Messaging):

    def __init__(self, task):
        self.__connected = False
        super().__init__(task)


    def is_connected(self) -> bool:
        try:
            self.ping()
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


    def ping(self) -> bool:
        try:
            logger.print_cmd('Send MQTT ping')
            self.__c.ping()
        except:
            raise MqttException("MQTT Ping failed. Connection unstable.")
            self.disconnect()
        return self.__connected


    def wait_msg(self):
        try:
            while 1:
                self.__c.wait_msg()
        finally:
            self.__c.disconnect()
