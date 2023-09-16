
import pytest
import asyncio

from core.config import Config
from domain.app import App
from domain.setup import SetupTask
from domain.health import HealthTask
from domain.mqtt_alive import MqttAliveTask
from adapter.internet import Internet
from adapter.wifi_mock import WifiMock
from adapter.mqtt_mock import MqttMock
from tests.health_check import HealthCheckTask



def test_create_task():
    task = SetupTask()



def test_run_task():
    app = App()
    Config.set("SETUP_INTERVAL_MS", 1)
    Config.set("HEALTH_INTERVAL_MS", 1)
    wifi = WifiMock()
    i = Internet(connection = wifi)
    mqtt = MqttMock("mock_test")
    app.set_networking(i)
    app.set_messaging(mqtt)
    setup_task = app.add_task( SetupTask(task_name="setup_task", app=app) )
    health_task = app.add_task( HealthTask(task_name="health_task", app=app) )
    mqtt_alive_task = app.add_task( MqttAliveTask(task_name="mqtt_alive_task", app=app) )
    health_check_task = app.add_task( HealthCheckTask(task_name="health_check_task", app=app) )
    asyncio.run(app.run())
