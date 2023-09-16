import time


from core.logger import Logger
from core.config import Config
from paho.mqtt.client import Client as MqttClient
from paho.mqtt.client import MQTT_LOG_DEBUG
import paho.mqtt.subscribe as subscribe
from domain.messaging import Messaging, MessagingException



def on_connect(client, userdata, flags, rc):
    print("connected")

#
# class
#
class MqttPaho(Messaging):

    def __init__(self, task_name):
        self.__client_id = Config.get("MQTT_CLIENT_ID")
        self.__mqtt_broker = Config.get("MQTT_BROKER")
        self.__mqtt_port = Config.get("MQTT_PORT")
        self.__mqtt_keepalive = Config.get("MQTT_KEEPALIVE")
        self.__mqtt_alive_topic = Config.get("MQTT_ALIVE_TOPIC")
#        self.__c.on_log = self.on_log
        self.reset()
        #self.__c.enable_logger(MQTT_LOG_DEBUG)
        super().__init__(task_name)
        self.LOG.print_info("initialized")



    def reset(self):
        self.__c = MqttClient(client_id=self.__client_id, clean_session=True)
        self.__c.on_connect = self.on_connect
        self.__c.on_disconnect = self.on_disconnect
        self.__c.on_message = self.on_message
        self.__connected = False


    def on_log(self, client, userdata, level, buf):
        print("log: ",buf)


    def on_connect(self, client, userdata, flags, rc):
        self.__connected = True
        self.LOG.print_info('Connected to MQTT Broker!')


    def on_disconnect(self, client, userdata, rc):
        self.__connected = True
        self.LOG.print_info('Disconnected from MQTT Broker!')

    def on_message(self, client, userdata, message, tmp=None):
        print(" Received message " + str(message.payload)
            + " on topic '" + message.topic
            + "' with QoS " + str(message.qos))


    def connect(self):
        self.LOG.print_cmd('Connecting to MQTT Broker')
        #import traceback
        #for line in traceback.format_stack():
        #    print(line.strip())
        self.__c.connect(self.__mqtt_broker, self.__mqtt_port, keepalive=self.__mqtt_keepalive)
        self.__c.loop_start()
        # self.is_connected()


    def disconnect(self, force=False):
        if self.__connected or force:
            self.LOG.print_cmd('Disconnecting from MQTT Broker')
            self.__connected = False
            self.__c.disconnect()
            self.reset()


    def publish(self, topic, msg):
        self.LOG.print_cmd('Publishing to MQTT topic: {}'.format(topic))
        self.__c.publish(topic, msg, qos=1)


    def on_message_print(self, client, userdata, message):
        print("%s %s" % (message.topic, message.payload))


    def subscribe(self, topic, message_func):
        self.LOG.print_cmd('Subscribing to MQTT topic: {}'.format(topic))
        #subscribe.callback(message_func, topic)
        self.__c.message_callback_add(topic, message_func)
        self.__c.subscribe(topic, 1)


    def send_alive(self):
        self.publish(self.__mqtt_alive_topic, "ALIVE")


    def ping(self) -> bool:
        try:
            self.LOG.print_cmd('Send MQTT ping')
            self.__c.ping()
        except:
            raise MqttException("MQTT Ping failed. Connection unstable.")
            self.disconnect()
        return self.__connected


    def is_connected(self) -> bool:
        try:
            self.ping()
            self.__connected = True
            self.LOG.print_info('Connected to MQTT Broker')
        except:
            self.disconnect(False)
        return self.__connected


    def wait_msg(self):
        try:
            while 1:
                self.__c.wait_msg()
        finally:
            self.__c.disconnect()
