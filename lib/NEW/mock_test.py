#!/usr/bin/env python3

from core.config import Config
from core.tasks import Task
from domain.app import App, AppException
from domain.setup import SetupTask
from domain.health import HealthTask
from domain.control import ControlTask
from adapter.mock_mqtt import MockMqtt
from tests.setup_check import SetupCheckTask
from tests.health_check import HealthCheckTask



import asyncio

class TestTask(Task):

    def __init__(self, task_name = "test_task", plus_number = 1, max_cycles = 3, sleep_s = 0.1):
        self.plus_number = plus_number
        self.max_cycles = max_cycles
        self.sleep_s = sleep_s
        super().__init__(task_name)

    async def task(self):
        self.LOG.print_info("task started!")
        i = 0
        while i < self.max_cycles:
            self.LOG.print_info("beep {}".format(i))
            await asyncio.sleep(self.sleep_s)
            i += self.plus_number


def main():
    app = App()
    Config.set("SETUP_INTERVAL_MS", 1)
    app.load_config('config.json')
    mqtt = MockMqtt("mock_test")
    app.set_messaging(mqtt)
    t1 = app.add_task( TestTask("test_task1", 1, 3))
    setup_task = app.add_task( SetupTask(task_name="setup_task", app=app) )
    health_task = app.add_task( HealthTask(task_name="health_task", app=app) )
    #boot_check_task = app.add_task( BootCheckTask(task_name="boot_check_task", app=app) )
    health_check_task = app.add_task( HealthCheckTask(task_name="health_check_task", app=app) )
    asyncio.run(app.run())


app = App()


if __name__ == '__main__':
    main()
