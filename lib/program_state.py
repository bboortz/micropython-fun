
import sys



# 
# global constants
#
MAX_ERRORS = 10
MAX_COUNTER = sys.maxsize - 1000


#
# class
#
#
# classes
#
class ProgramStateException(BaseException):
    pass


class ProgramState:

    def __init__(self, dev, led, sensors, wdt):
        self.setup_counter = 0
        self._setup_done = False
        self.max_setup_attempts = 2
        self.counter = 0
        self.err_counter = 0
        self.max_errors = MAX_ERRORS
        self.max_counter = MAX_COUNTER
        self.dev = dev
        self.led = led
        self.sensors = sensors
        self.wdt = wdt
        self.wifi = None
        self.mqtt = None

    def is_setup_done(self):
        return self._setup_done

    def setup_done(self):
        self._setup_done = True
        self.setup_counter = 0

    # TODO
    def setup_undone(self):
        self._setup_done = False
