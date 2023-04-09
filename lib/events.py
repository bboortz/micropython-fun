from config import CONFIG

import sys
import time
import json
import logger
from machine import soft_reset as sreset


class EventsException(BaseException):
    pass


class Events:

    def __init__(self, filename, stage, location, device, mqtt = None):
        self.filename = filename
        self.stage = stage
        self.location = location
        self.device = device
        self.mqtt = mqtt


    def setup_mqtt(self, mqtt):
        self.mqtt = mqtt

    def event(self, etype, event, counter = 0):
        # log to stdout
        if etype == "info":
            logger.print_info(event)
        elif etype == "cmd":
            logger.print_info(event)
        else:
            logger.print_error(event)

        json_data = {
            "type": etype,
            "stage": self.stage,
            "location": self.location,
            "device": self.device,
            "event": event,
            "measure_count": counter,
            "ticks_s": 0,
        }

        # log to file
        json_str = json.dumps(json_data)
        f = open(self.filename, 'a')
        f.write(json_str)
        f.write('\n')
        f.close()

    def soft_reset(self):
        self.event("cmd", "soft reset")
        sreset()
