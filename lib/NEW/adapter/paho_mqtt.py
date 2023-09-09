import time


from core.logger import Logger
from core.config import Config
from paho.mqtt.client import Client as MqttClient
from paho.mqtt.client import MQTT_LOG_DEBUG
from adapter.mqtt import Mqtt


def on_connect(client, userdata, flags, rc):
    print("connected")

#
# class
#
class PahoMqtt(Mqtt):

    def __init__(self, task_name):
        self.__client_id = Config.get("MQTT_CLIENT_ID")
        self.__mqtt_broker = Config.get("MQTT_BROKER")
        self.__mqtt_port = Config.get("MQTT_PORT")
        self.__mqtt_keepalive = Config.get("MQTT_KEEPALIVE")
        self.__c = MqttClient(client_id=self.__client_id)
        self.__c.on_log = self.on_log
        self.__c.on_connect= self.on_connect
        #self.__c.enable_logger(MQTT_LOG_DEBUG)
        super().__init__(task_name)
        self.LOG.print_info("initialized")


    def on_log(self,client, userdata, level, buf):
        print("log: ",buf)

    def on_connect(self,client, userdata, flags, rc):
        print("connected")

    def is_connected(self) -> bool:
        try:
            self.ping()
            self.__connected = True
            self.LOG.print_info('Connected to MQTT Broker')
        except:
            self.disconnect(False)
        return self.__connected


    def connect(self):
        self.LOG.print_cmd('Connecting to MQTT Broker')
        self.__c.connect(self.__mqtt_broker, self.__mqtt_port, keepalive=self.__mqtt_keepalive)
        self.__c.loop_start()
        # self.is_connected()


    def disconnect(self, force=False):
        if self.__connected or force:
            self.LOG.print_cmd('Disconnected from MQTT Broker')
            self.__connected = False
            self.__c.disconnect()


    def publish(self, topic, msg):
        self.LOG.print_cmd('Publish data via MQTT topic: {}'.format(topic))
        self.__connected = False
        self.__c.publish(topic, msg, qos=2)


    def subscribe(self, topic, message_func):
        self.LOG.print_cmd('Subscribe data vi MQTT')
        self.__c.set_callback(message_func)
        self.__c.subscribe(topic)


    def ping(self) -> bool:
        try:
            self.LOG.print_cmd('Send MQTT ping')
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
