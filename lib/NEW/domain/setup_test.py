
import pytest
import asyncio

from core.config import Config
from domain.app import App
from domain.setup import SetupTask
from adapter.mock_mqtt import MockMqtt
from tests.setup_check import SetupCheckTask



def test_create_task():
    task = SetupTask()



def test_run_task():
    app = App()
    Config.set("SETUP_INTERVAL_MS", 1)
    mqtt = MockMqtt("mock_test")
    app.set_messaging(mqtt)
    setup_task = app.add_task( SetupTask(task_name="setup_task", app=app) )
    setup_check_task = app.add_task( SetupCheckTask(task_name="setup_check_task", app=app) )
    asyncio.run(app.run())
