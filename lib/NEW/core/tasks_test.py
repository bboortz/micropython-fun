
import pytest
import asyncio

from core.tasks import Tasks, TaskException


def test_create_tasks():
    t = Tasks()


def test_get_task_list():
    t = Tasks()
    task_list = t.get_task_list()
    assert task_list == []


test_gather_all_tasks_var = False
def test_gather_all_tasks():
    async def test_task():
        global test_gather_all_tasks_var
        test_gather_all_tasks_var = True
        print("lala")

    t = Tasks()
    t1 = t.add_task("test_task1", test_task() )
    asyncio.run( t.gather_all_tasks() )
    assert test_gather_all_tasks_var == True

