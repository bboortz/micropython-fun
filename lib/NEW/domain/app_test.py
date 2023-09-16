
import pytest
import asyncio

from domain.app import App, AppException
from core.tasks import Task
from core.state import STATE_INIT, STATE_STOPPED
from adapter.internet import Internet
from adapter.wifi_mock import WifiMock 
from adapter.mqtt_paho import MqttPaho

app_test_task_var = False
class AppTestTask(Task):

    def __init__(self, task_name = "test_task"):
        super().__init__(task_name)
        self.LOG.print_info("task created!")

    async def task(self):
        global app_test_task_var
        app_test_task_var = True
        print("lala")


def test_create_app():
    app = App()


def test_run():
    app = App()
    asyncio.run(app.run())


def test_run_with_config():
    app = App()
    app.load_config('./config_test.json')
    asyncio.run(app.run())


def test_get_state():
    app = App()
    app.get_state()


def test_get_current_state():
    app = App()
    assert app.get_current_state() == STATE_INIT
    app.load_config('./config_test.json')
    asyncio.run(app.run())
    assert app.get_current_state() == STATE_STOPPED


def test_run_with_tasks():
    app = App()
    t1 = app.add_task( AppTestTask() )
    asyncio.run(app.run())
    assert app_test_task_var == True


def test_set_networking():
    app = App()
    assert app.get_networking() == None
    wifi = WifiMock()
    i = Internet(connection = wifi)
    app.set_networking(i)
    assert app.get_networking() != None


def test_set_messaging():
    app = App()
    assert app.get_messaging() == None
    mqtt = MqttPaho("test")
    app.set_messaging(mqtt)
    assert app.get_messaging() != None


def test_raise_app_exception():
    app = App()
    with pytest.raises(AppException):
        app.raise_app_exception("This exception must be catched by pytest!", "just a test!")


def test_noop():
    pass

