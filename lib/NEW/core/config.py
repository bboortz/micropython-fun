
import uuid
import json

from core.generic import GenericClass, GenericException
from core.logger import Logger



#
# class
#
class ConfigException(GenericException):
    def __init__(self, message, cause):
        context = "config"
        super().__init__(context, message, cause)


class Config:
    host = str(uuid.uuid4()).split("-")[0]
    topic_prefix = "sensornet"
    __default_conf = {
        "STAGE": "dev",
        "LOCATION": "unknown",
        "HOST": host,
        "LOG_DEBUG": False,
        "BOOT_WAIT_MS": 1000,
        "SETUP_INTERVAL_MS": 3000,
        "SETUP_MAX_INITS": 3,
        "SETUP_MAX_ATTEMPTS": 3,
        "HEALTH_INTERVAL_MS": 5000,
        "HEALTHY_AFTER_POSITIVE_CHECKS": 2,
        "UNHEALTHY_AFTER_NEGATIVE_CHECKS": 2,
        "MQTT_BROKER": "localhost",
        "MQTT_PORT": 1883,
        "MQTT_CLIENT_ID": host,
        "MQTT_KEEPALIVE": 5,
        "MQTT_ALIVE_TOPIC": topic_prefix + "/mqtt/alive",
        "MQTT_MAX_CONNECT_ATTEMPTS": 3,
        "MQTT_CONNECT_TIMEOUT": 3
    }
    __conf = __default_conf
    LOG = Logger("core.config.Config", "core")


    @staticmethod
    def load(filename: str):
        Config.LOG.print_cmd("Loading config file {}".format(filename))
        with open(filename) as f_in:
            json_dict = json.load(f_in)
            for attr in json_dict:
                Config.__conf[attr] = json_dict[attr]
        Config.print()


    @staticmethod
    def get(name):
        if not name in Config.__default_conf:
            raise ConfigException("attribute {} not found in config".format(name), "attribute {} is not set in config".format(name))

        return Config.__conf[name]


    @staticmethod
    def set(name, value):
        Config.__conf[name] = value


    @staticmethod
    def print():
        Config.LOG.print_info("Config: {}".format(Config.__conf))



