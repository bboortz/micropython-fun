import time


from core.logger import Logger
from core.config import Config
from paho.mqtt.client import Client as MqttClient
from paho.mqtt.client import MQTT_LOG_DEBUG
from adapter.mqtt import Mqtt


#
# class
#
class MockMqtt(Mqtt):

    def __init__(self, task_name):
        super().__init__(task_name)
        self.LOG.print_info("initialized")


    def is_connected(self) -> bool:
        return True


    def connect(self):
        self.LOG.print_cmd('Connecting to MQTT Broker')


    def disconnect(self, force=False):
        self.LOG.print_info('Disconnected from MQTT Broker')


    def publish(self, topic, msg):
        self.LOG.print_cmd('Publish data via MQTT topic: {}'.format(topic))


    def subscribe(self, topic, message_func):
        self.LOG.print_cmd('Subscribe data vi MQTT')


    def ping(self) -> bool:
        self.LOG.print_cmd('Sending a MQTT ping')


    def wait_msg(self):
        self.LOG.print_cmd('Waiting for a MQTT message')
