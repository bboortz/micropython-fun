
try:
    import uasyncio as asyncio
except:
    import asyncio

from core.generic import GenericClass, GenericException
from core.config import Config
from core.tasks import Tasks
from core.state import State



#
# class
#
class AppException(GenericException):
    def __init__(self, message, cause):
        context = "app"
        super().__init__(context, message, cause)



class App(GenericClass):

    def __init__(self, task = "domain"):
        self.__state = State()
        self.__tasks = Tasks()
        self.__networking = None
        self.__messaging = None
        super().__init__(task)
        self.LOG.print_debug("initialized")


    def load_config(self, filename: str):
        Config.load(filename)


    def get_state(self):
        return self.__state


    def get_current_state(self):
        return self.__state.state


    def add_task(self, task):
        return self.__tasks.add_task(task)


    def set_networking(self, networking):
        self.__networking = networking


    def get_networking(self):
        return self.__networking


    def set_messaging(self, messaging):
        self.__messaging = messaging


    def get_messaging(self):
        return self.__messaging


    async def run(self):
        self.LOG.print_cmd("running program")
        await asyncio.sleep( Config.get("BOOT_WAIT_MS") / 1000 )
        await self.__tasks.gather_all_tasks()
        self.LOG.print_info("end of run() function")
        self.__state.to_stopped()


    def raise_app_exception(self, msg, cause):
        raise AppException(msg, cause);

