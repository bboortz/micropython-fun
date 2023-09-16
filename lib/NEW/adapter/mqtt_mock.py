import time


from core.logger import Logger
from core.config import Config
from paho.mqtt.client import Client as MqttClient
from paho.mqtt.client import MQTT_LOG_DEBUG
from domain.messaging import Messaging


#
# class
#
class Message:
    def __init__(self, mid):
        self.mid = mid


class MqttMock(Messaging):

    def __init__(self, task_name = "setup_task"):
        self.__mqtt_alive_topic = Config.get("MQTT_ALIVE_TOPIC")
        self.__on_message_callback = None
        super().__init__(task_name)
        self.LOG.print_info("initialized")


    def is_connected(self) -> bool:
        return True


    def connect(self):
        self.LOG.print_cmd('Connecting to MQTT Broker')


    def disconnect(self, force=False):
        self.LOG.print_info('Disconnected from MQTT Broker')


    def publish(self, topic, msg):
        self.LOG.print_cmd('Publishing data to MQTT topic: {}'.format(topic))
        if self.__on_message_callback != None:
            print("callback")
            self.__on_message_callback("test-client", "userdata", Message(mid = 1) )


    def subscribe(self, topic, message_func):
        self.LOG.print_cmd('Subscribing data to MQTT topic: {}'.format(topic))
        self.__on_message_callback = message_func


    def send_alive(self):
        self.publish(self.__mqtt_alive_topic, "ALIVE")


    def ping(self) -> bool:
        self.LOG.print_cmd('Sending a MQTT ping')


    def wait_msg(self):
        self.LOG.print_cmd('Waiting for a MQTT message')
