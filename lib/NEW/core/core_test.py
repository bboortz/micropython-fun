
import pytest
import asyncio

from core.core import Core, CoreException
from core.tasks import Task
from core.state import *

core_test_task_var = False
class CoreTestTask(Task):

    def __init__(self, task_name = "test_task"):
        super().__init__(task_name)
        self.LOG.print_info("task created!")

    async def task(self):
        global core_test_task_var
        core_test_task_var = True
        print("lala")


def test_create_core():
    c = Core()


def test_run():
    c = Core()
    asyncio.run(c.run())


def test_run_with_config():
    c = Core()
    c.load_config('./config_test.json')
    asyncio.run(c.run())


def test_get_state():
    c = Core()
    assert c.get_state() == STATE_INIT
    c.load_config('./config_test.json')
    asyncio.run(c.run())
    assert c.get_state() == STATE_STOPPED


def test_run_with_tasks():
    c = Core()
    t1 = c.add_task( CoreTestTask() )
    asyncio.run(c.run())
    assert core_test_task_var == True


def test_raise_core_exception():
    c = Core()
    with pytest.raises(CoreException):
        c.raise_core_exception("This exception must be catched by pytest!", "just a test!")


def test_noop():
    pass

