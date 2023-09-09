
import asyncio

from core.generic import GenericClass
from core.logger import Logger
from core.config import Config
from core.tasks import Task
from core.state import State
from domain.app import App



#
# global constants
#
DEFAULT_APP = App()



#
# classes
#
class SetupTask(Task):

    def __init__(self, task_name = "setup_task", app = DEFAULT_APP):
        self.app = app
        self.state = app.get_state()
        self.mqtt = app.get_messaging()
        super().__init__(task_name)

    async def task(self):
        self.LOG.print_info("task started!")

        while True:
            await asyncio.sleep( Config.get("SETUP_INTERVAL_MS") / 1000 )
            if not self.state.is_running():
                self.LOG.print_info("everything stopped! exiting task now!")
                break

            if self.state.is_setup_done():
                self.LOG.print_info("setup is already done!")
                continue

            self.state.to_in_setup()
            self.mqtt.connect()
            self.state.to_setup_done()
            self.LOG.print_info("setup is done!")
