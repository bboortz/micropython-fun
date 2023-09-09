
import sys
import time
import json

from core.generic import GenericClass, GenericException
from core.logger import Logger



# 
# global constants
#
STATE_UNKNOWN = 0
STATE_INIT = 1
STATE_STOPPED = 10
STATE_IN_SETUP = 100
STATE_SETUP_DONE = 150
STATE_HEALTHY = 200
STATE_UNHEALTHY = 300
STATE_DICT = {
    0:   "STATE_UNKNOWN",
    1:   "STATE_INIT",
    10:  "STATE_STOPPED",
    100: "STATE_IN_SETUP",
    150: "STATE_SETUP_DONE",
    200: "STATE_HEALTHY",
    300: "STATE_UNHEALTHY"
}



#
# class
#
class StateException(GenericException):
    def __init__(self, message, cause):
        context = "state"
        super().__init__(context, message, cause)


class State(GenericClass):

    def __init__(self, task = "main"):
        self.setup_counter = 0
        self.state = STATE_INIT
        self.__setup_done = False
        super().__init__(task)


    def is_running(self):
        return (self.state != STATE_STOPPED)


    def is_healthy(self):
        return (self.state == STATE_HEALTHY)


    def is_setup_done(self):
        return self.__setup_done


    def setup_done(self):
        self.__setup_done = True
        self.setup_counter = 0


    def setup_undone(self):
        self.__setup_done = False


    def set_state(self, state: int):
        curr_state_str = format(STATE_DICT[self.state])
        next_state_str = format(STATE_DICT[state])


        if state != STATE_INIT  and  state != STATE_STOPPED:
            if self.state == state:
                raise StateException("Cannot go from state {} to {}.".format(curr_state_str, next_state_str), "State is unchanged!")

            if self.state == STATE_UNKNOWN:
                if state != STATE_INIT:
                    raise StateException("Cannot go from state {} to {}.".format(curr_state_str, next_state_str), "State has been changed in a unsupported order!")

            elif self.state == STATE_INIT:
                if state != STATE_IN_SETUP:
                    raise StateException("Cannot go from state {} to {}.".format(curr_state_str, next_state_str), "State has been changed in a unsupported order!")

            elif self.state == STATE_STOPPED:
                if state != STATE_INIT:
                    raise StateException("Cannot go from state {} to {}.".format(curr_state_str, next_state_str), "State has been changed in a unsupported order!")

            elif self.state == STATE_IN_SETUP:
                if state != STATE_SETUP_DONE:
                    raise StateException("Cannot go from state {} to {}.".format(curr_state_str, next_state_str), "State has been changed in a unsupported order!")

            elif self.state == STATE_SETUP_DONE:
                if state != STATE_HEALTHY  and  state != STATE_UNHEALTHY:
                    raise StateException("Cannot go from state {} to {}.".format(curr_state_str, next_state_str), "State has been changed in a unsupported order!")

            elif self.state == STATE_HEALTHY:
                if state == STATE_SETUP_DONE:
                    raise StateException("Cannot go from state {} to {}.".format(curr_state_str, next_state_str), "State has been changed in a unsupported order!")

            elif self.state == STATE_UNHEALTHY:
                if state == STATE_SETUP_DONE:
                    raise StateException("Cannot go from state {} to {}.".format(curr_state_str, next_state_str), "State has been changed in a unsupported order!")

            self.LOG.print_info( "** {} **".format(STATE_DICT[state]) )
        self.state = state


    def to_init(self):
        self.set_state(STATE_INIT)
        self.setup_undone()


    def to_stopped(self):
        self.set_state(STATE_STOPPED)


    def to_in_setup(self):
        self.set_state(STATE_IN_SETUP)
        self.setup_undone()


    def to_setup_done(self):
        self.set_state(STATE_SETUP_DONE)
        self.setup_done()


    def to_healthy(self):
        self.set_state(STATE_HEALTHY)


    def to_unhealthy(self):
        self.set_state(STATE_UNHEALTHY)
