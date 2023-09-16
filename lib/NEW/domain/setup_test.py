
import pytest
import asyncio

from core.config import Config
from domain.app import App
from domain.setup import SetupTask
from adapter.internet import Internet
from adapter.wifi_mock import WifiMock
from adapter.mqtt_mock import MqttMock
from tests.setup_check import SetupCheckTask



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
    setup_check_task = app.add_task( SetupCheckTask(task_name="setup_check_task", app=app) )
    asyncio.run(app.run())
