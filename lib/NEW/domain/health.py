
import asyncio

from core.config import Config
from core.tasks import Task
from core.state import State
from domain.app import App
from domain.messaging import MessagingException



#
# global constants
#
DEFAULT_APP = App()



#
# classes
#
class HealthTask(Task):

    def __init__(self, task_name = "setup_task", app = DEFAULT_APP):
        self.app = app
        self.state = app.get_state()
        self.mqtt = app.get_messaging()
        self.reset()
        self.error_count = 0
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

            if self.check_counter == 0:
                self.mqtt.subscribe(Config.get("MQTT_ALIVE_TOPIC"), self.on_mqtt_message)

            if self.state.is_unhealthy():
                if self.mqtt_connect_counter > Config.get("MQTT_MAX_CONNECT_ATTEMPTS"):
                    self.state.to_init()

                try:
                    self.mqtt_connect_counter += 1
                    self.mqtt.connect()
                    self.mqtt.subscribe(Config.get("MQTT_ALIVE_TOPIC"), self.on_mqtt_message)
                    self.state.to_setup_done()
                    self.reset()
                except Exception:
                    self.LOG.print_error("Unable to connect to MQTT broker!")

            elif self.state.is_setup_done():
                print("counter: ", self.check_counter, self.last_positive_counter, self.positive_counter, self.last_message_id)
                self.check_counter += 1
                if self.check_counter - self.last_message_id > Config.get("UNHEALTHY_AFTER_NEGATIVE_CHECKS"):
                    print("disconnect..")
                    self.state.to_unhealthy()
                    self.mqtt.disconnect()
                    self.reset()


    def reset(self):
        self.check_counter = 0
        self.last_message_id = 0
        self.mqtt_connect_counter = 0
        self.positive_counter = 0
        self.last_positive_counter = 0


    def on_mqtt_message(self, client, userdata, message):
        self.LOG.print_info("healthy id: {}".format(message.mid))
        self.last_positive_counter = self.positive_counter
        self.positive_counter += 1
        self.last_message_id = message.mid
        if not self.state.is_healthy():
            if self.positive_counter >= Config.get("HEALTHY_AFTER_POSITIVE_CHECKS"):
                self.state.to_healthy()

