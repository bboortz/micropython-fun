
import pytest
import asyncio

from core.config import Config
from domain.app import App
from domain.setup import SetupTask
from domain.health import HealthTask
from domain.mqtt_alive import MqttAliveTask
from adapter.mock_mqtt import MockMqtt
from tests.health_check import HealthCheckTask



def test_create_task():
    task = SetupTask()



def test_run_task():
    app = App()
    Config.set("SETUP_INTERVAL_MS", 1)
    Config.set("HEALTH_INTERVAL_MS", 1)
    mqtt = MockMqtt("mock_test")
    app.set_messaging(mqtt)
    app.add_task( SetupTask(task_name="setup_task", app=app) )
    app.add_task( HealthTask(task_name="health_task", app=app) )
    app.add_task( MqttAliveTask(task_name="mqtt_alive_task", app=app) )
    app.add_task( HealthCheckTask(task_name="health_check_task", app=app) )
    asyncio.run(app.run())
