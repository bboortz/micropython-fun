
try:
    import uasyncio as asyncio
except:
    import asyncio

from core.generic import GenericClass, GenericException
from core.config import Config
from core.tasks import Tasks



#
# class
#
class CoreException(GenericException):
    def __init__(self, message, cause):
        context = "core"
        super().__init__(context, message, cause)



class Core(GenericClass):

    def __init__(self, task = "main"):
        self.__run = False
        self.__tasks = Tasks()
        super().__init__(task)
        self.LOG.print_info("initialized")


    def load_config(self, filename: str):
        Config.load(filename)


    def add_tasks(self, task_name, coro):
        return self.__tasks.add_task(task_name, coro)


    async def run(self):
        self.LOG.print_cmd("running program")
        await asyncio.sleep( Config.get("BOOT_WAIT_MS") / 1000 )
        await self.__tasks.gather_all_tasks()
        self.LOG.print_info("end of run() function")


    def raise_core_exception(self, msg, cause):
        raise CoreException(msg, cause);

