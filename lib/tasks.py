import logger
import time
import uasyncio as asyncio

# 
# global constants
#



#
# class
#
class TaskException(BaseException):
    pass



class Task:

    def __init__(self, task_name, asyncio_task):
        self.task_name = task_name
        self.asyncio_task = asyncio_task


class Tasks:

    def __init__(self):
        self.__tasks_list = []


    def create_task(self, task_name, coro):
        asyncio_task = asyncio.create_task(coro)
        t = Task(task_name, asyncio_task)
        self.__tasks_list.append(t)
        logger.print_info("Task created: %s" % task_name)
        return asyncio_task

    def cancel_task(self, task):
        logger.print_info("Cancel task: %s" % task.task_name)
        task.asyncio_task.cancel()
        logger.print_info("Task cancelled: %s" % task.task_name)

    def cancel_all_tasks(self):
        for t in self.__tasks_list:
            try:
                self.cancel_task(t)
            except:
                logger.print_error("Cancel task failed: %s" % t.task_name)
            self.__tasks_list.remove(t)
