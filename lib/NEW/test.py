#!/usr/bin/env python3

from domain.app import App, AppException
from core.tasks import Task
from adapter.mock_mqtt import MockMqtt



import asyncio

class TestTask(Task):

    def __init__(self, task_name = "test_task", plus_number = 1, max_cycles = 3, sleep_s = 0.1):
        self.plus_number = plus_number
        self.max_cycles = max_cycles
        self.sleep_s = sleep_s
        super().__init__(task_name)

    async def task(self):
        i = 0
        from core.logger import Logger
        while i < self.max_cycles:
            self.LOG.print_info("beep {}".format(i))
            await asyncio.sleep(self.sleep_s)
            i += self.plus_number


def main():
    app = App()
    app.load_config('config.json')
    mqtt = MockMqtt("test")
    app.set_messaging(mqtt)
    t1 = app.add_task( TestTask("test_task1", 1, 3))
    t2 = app.add_task( TestTask("test_task2", 2, 3))
    asyncio.run(app.run())


if __name__ == '__main__':
    main()
