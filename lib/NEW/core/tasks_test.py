
import pytest
import asyncio

from core.tasks import Task, Tasks, TaskException


tasks_test_task_var = False
class TasksTestTask(Task):

    def __init__(self, task_name = "test_task"):
        super().__init__(task_name)
        self.LOG.print_info("task created!")

    async def task(self):
        global tasks_test_task_var
        tasks_test_task_var = True
        print("lala")


def test_create_tasks():
    t = Tasks()


def test_get_task_list():
    t = Tasks()
    task_list = t.get_task_list()
    assert task_list == []


def test_gather_all_tasks():
    t = Tasks()
    t1 = t.add_task( TasksTestTask() )
    asyncio.run( t.gather_all_tasks() )
    assert tasks_test_task_var == True

