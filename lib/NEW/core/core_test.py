
import pytest
import asyncio

from core.core import Core, CoreException


def test_create_core():
    c = Core()


def test_run():
    c = Core()
    asyncio.run(c.run())


def test_run_with_config():
    c = Core()
    c.load_config('./config_test.json')
    asyncio.run(c.run())


test_run_with_tasks_var = False
def test_run_with_tasks():
    async def test_task():
        global test_run_with_tasks_var
        test_run_with_tasks_var = True

    c = Core()
    t1 = c.add_tasks("test_task1", test_task() )
    asyncio.run(c.run())
    assert test_run_with_tasks_var == True


def test_raise_core_exception():
    c = Core()
    with pytest.raises(CoreException):
        c.raise_core_exception("This exception must be catched by pytest!", "just a test!")


def test_noop():
    pass

