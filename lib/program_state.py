
import sys
import time
import json
import logger



# 
# global constants
#
MAX_SETUP_ATTEMPTS = 2
MAX_ERRORS = 10
MAX_COUNTER = sys.maxsize - 1000
STATE_UNKNOWN = 0
STATE_STOPPED = 1
STATE_IN_SETUP = 100
STATE_SETUP_DONE = 150
STATE_HEALTHY = 200
STATE_UNHEALTHY = 300


#
# class
#
#
# classes
#
class ProgramStateException(BaseException):
    pass


class ProgramState:

    def __init__(self, stage, location, host, dev, mqtt_topic_states):
        self.setup_counter = 0
        self.state = STATE_IN_SETUP
        self._setup_done = False
        # TODO: here or in boot.py
        self.max_setup_attempts = MAX_SETUP_ATTEMPTS
        self.counter = 0
        self.err_counter = 0
        self.max_errors = MAX_ERRORS
        self.max_counter = MAX_COUNTER
        self.stage = stage
        self.location = location
        self.host = host
        self.dev = dev
        self.led = dev.status_led
        self.sensors = dev.sensors
        self.wdt = dev.wdt
        self.wifi = None
        self.mqtt = None
        self.mqtt_topic_states = mqtt_topic_states

    def is_stopped(self):
        return (self.state == STATE_STOPPED)

    def is_setup_done(self):
        return self._setup_done

    def setup_done(self):
        self._setup_done = True
        self.setup_counter = 0

    def setup_undone(self):
        self._setup_done = False

    def set_state_unhealthy(self):
        logger.print_info("** STATE_UNHEALTHY **")
        self.state = STATE_UNHEALTHY
        self.send_state_via_mqtt(self.state)
        self.setup_undone()

    def set_state_in_setup(self):
        logger.print_info("** STATE_IN_SETUP **")
        self.state = STATE_IN_SETUP
        self.send_state_via_mqtt(self.state)

    def set_state_setup_done(self):
        logger.print_info("** STATE_SETUP_DONE **")
        self.state = STATE_SETUP_DONE
        self.send_state_via_mqtt(self.state)
        self.setup_done()

    def set_state_stopped(self):
        logger.print_info("** STATE_STOPPED **")
        self.state = STATE_STOPPED
        self.send_state_via_mqtt(self.state)
        self.setup_undone()

    def set_state_healthy(self):
        logger.print_info("** STATE_HEALTY **")
        self.state = STATE_HEALTHY
        self.send_state_via_mqtt(self.state)

    def send_state_via_mqtt(self, state, counter = 0):

        datetime = str(time.localtime())
        ticks_s = int(time.ticks_ms() / 1000)

        json_data = {
            "type": "info",
            "stage": self.stage,
            "location": self.location,
            "device": self.host,
            "state": state,
            "measure_count": counter,
            "datetime": datetime,
            "ticks_s": ticks_s,
        }

        json_str = json.dumps(json_data)
        if self.mqtt != None:
            # log to mqtt
            self.mqtt.publish(self.mqtt_topic_states, json_str)
