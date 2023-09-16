
try:
    import uasyncio as asyncio
except:
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
        self.network = app.get_networking()
        self.mqtt = app.get_messaging()
        self.init_counter = 0
        self.reset()
        super().__init__(task_name)

    async def task(self):
        self.LOG.print_info("task started!")

        while True:
            await asyncio.sleep( Config.get("SETUP_INTERVAL_MS") / 1000 )
            if not self.state.is_running():
                self.LOG.print_info("everything stopped! exiting task now!")
                break

            if self.state.is_setup_done():
                self.LOG.print_debug("setup is already done!")
                continue
            
            if self.state.is_init():
                self.reset()
                self.state.to_in_setup()

            if self.init_counter >= Config.get("SETUP_MAX_INITS"):
                self.LOG.print_error("Unable to init & setup. {} attempts failed. Soft-reset!".format(self.init_counter))
                # TODO!!!!!!!!!!!!!!!
                import sys
                sys.exit(1) # TODO !!!!!!!!!!!!!!!!!!
                continue

            if self.setup_counter >= Config.get("SETUP_MAX_ATTEMPTS"):
                self.LOG.print_error("Unable to setup. {} attempts failed. Trying to initialize again.".format(self.setup_counter))
                self.init_counter += 1
                self.state.to_init()
                continue

            try:
                self.setup_counter += 1
                if self.network != None:
                    self.network.connect()
                    if self.mqtt != None: 
                        self.mqtt.connect()
                self.state.to_setup_done()
                self.LOG.print_debug("setup is done!")
            except Exception:
                self.LOG.print_error("Unable to connect to MQTT broker!")


    def reset(self):
        self.setup_counter = 0
        if self.mqtt != None:
            self.mqtt.disconnect()


