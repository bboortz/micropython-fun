
import asyncio
import sys

from core.config import Config
from core.tasks import Task
from domain.app import App



#
# global constants
#
DEFAULT_APP = App()
MAX_POSITIVE_CHECKS = 1



#
# classes
#
class HealthCheckTask(Task):

    def __init__(self, task_name = "health_check_task", app = DEFAULT_APP):
        self.app = app
        self.state = app.get_state()
        super().__init__(task_name)

    async def task(self):
        self.LOG.print_info("task started!")

        i = 0
        while True:
            await asyncio.sleep( Config.get("SETUP_INTERVAL_MS") / 1000 )
            if not self.state.is_running():
                self.LOG.print_info("everything stopped! exiting task now!")
                break

            if self.state.is_healthy():
                i += 1
                if i >= MAX_POSITIVE_CHECKS:
                    self.LOG.print_info("program is healthy! program will be stopped!")
                    self.state.to_stopped()
