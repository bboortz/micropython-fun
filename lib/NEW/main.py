#!/usr/bin/env python3

import sys
import asyncio

from core.config import Config
from core.generic import GenericException
from domain.app import App
from domain.setup import SetupTask
from domain.health import HealthTask
from domain.control import ControlTask
from adapter.paho_mqtt import PahoMqtt



def main():
    while True:
        try:
            app = App()
            Config.set("SETUP_INTERVAL_MS", 1)
            app.load_config('config.json')
            mqtt = PahoMqtt(task_name = "main")
            app.set_messaging(mqtt)
            setup_task = app.add_task( SetupTask(task_name="setup_task", app=app) )
            health_task = app.add_task( HealthTask(task_name="health_task", app=app) )
            asyncio.run(app.run())
        #except KeyboardInterrupt:
        #    pass
            #EVENTS.event("error", "Ctrl-C", program_state.counter)
            #health_t.cancel()
            #health_t = None
        except GenericException as ge:
            #EVENTS.event("error", "Failed in main() function because of an GenericException!")
            ge.print()
            #sys.print_exception(e)
            #EVENTS.soft_reset()
        #except:
        #    pass
            #EVENTS.event("error", "Failed in main() function because of an *UNCATCHED* Exception!", program_state.counter)
            #EVENTS.soft_reset()


if __name__ == '__main__':
    main()
