
try:
    import uasyncio as asyncio
except:
    import asyncio

from core.config import Config
from core.tasks import Task
from domain.app import App



#
# global constants
#
DEFAULT_APP = App()



#
# classes
#
class MqttAliveTask(Task):

    def __init__(self, task_name = "mqtt_alive_task", app = DEFAULT_APP):
        self.app = app
        self.state = app.get_state()
        self.mqtt = app.get_messaging()
        super().__init__(task_name)


    async def task(self):
        self.LOG.print_info("task started!")

        while True:
            await asyncio.sleep( Config.get("HEALTH_INTERVAL_MS") / 1000 )
            if not self.state.is_running():
                self.LOG.print_info("everything stopped! exiting task now!")
                break

            if not self.state.is_setup_done():
                self.LOG.print_debug("setup NOT done!")
                continue

            self.LOG.print_debug("ALIVE!")
            self.mqtt.send_alive()
