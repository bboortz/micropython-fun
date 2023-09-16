
import pytest
try:
    import uasyncio as asyncio
except:
    import asyncio

from core.config import Config
from adapter.mqtt_mock import MqttMock



def test_create_mqtt():
    w = MqttMock()


def test_mqtt_connect():
    w = MqttMock()
    w.connect()


def test_mqtt_connect_disconnect():
    w = MqttMock()
    w.connect()
    w.disconnect()


def test_mqtt_publish():
    w = MqttMock()
    w.connect()
    w.publish("topic/test", "test-message")
    w.disconnect()


