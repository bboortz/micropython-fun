
import time
try:
    import uasyncio as asyncio
except:
    import asyncio

from core.generic import GenericClass, GenericException
from core.logger import Logger



#
# class
#
class TaskException(GenericException):
    def __init__(self, message, cause):
        context = "task"
        super().__init__(context, message, cause)




class Task:

    def __init__(self, task_name, asyncio_task):
        self.task_name = task_name
        self.asyncio_task = asyncio_task



class Tasks(GenericClass):

    def __init__(self, task = "main"):
        self.__tasks_list = []
        super().__init__(task)


    def get_task_list(self):
        return self.__tasks_list


    def add_task(self, task_name, coro):
        asyncio_task = coro
        t = Task(task_name, asyncio_task)
        self.__tasks_list.append(t)
        self.LOG.print_info("Task added: %s" % task_name)
        return asyncio_task


#    async def run_all_tasks(self):
#        self.LOG.print_cmd("Run all tasks")
#        for t in self.__tasks_list:
#            asyncio.create_task(t.asyncio_task)


    async def gather_all_tasks(self):
        self.LOG.print_cmd("Run and gather all tasks")
        coro_dict = []
        for t in self.get_task_list():
            coro_dict.append(t.asyncio_task)
        await asyncio.gather(*coro_dict)


#    def cancel_task(self, task):
#        self.LOG.print_info("Cancel task: %s" % task.task_name)
#        task.asyncio_task.cancel()
#        self.LOG.print_info("Task cancelled: %s" % task.task_name)


#    def cancel_all_tasks(self):
#        for t in self.__tasks_list:
#            try:
#                self.cancel_task(t)
#            except:
#                self.LOG.print_error("Cancel task failed: %s" % t.task_name)
#            self.__tasks_list.remove(t)
