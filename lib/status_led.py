import logger
from machine import Pin
import neoled



# 
# global constants
#
TYPE_LED = "LED"
TYPE_NEOLED = "NEOLED"
NEOLED_COLOR_ON = (2, 2, 2)
NEOLED_COLOR_OFF = (0, 0, 0)



#
# class
#
class StatusLedException(BaseException):
    pass


class StatusLed:

    def __init__(self, config):
        self.__status_led_config = config.get("STATUS_LED")
        self.__led = None

        if self.__status_led_config != None:
            self.__led_type = self.__status_led_config.get("TYPE")
            self.__led_pin = self.__status_led_config.get("PIN")

            if self.__led_type == TYPE_NEOLED:
                led = Pin(self.__led_pin, Pin.OUT)
                self.__led = neoled.NeoLed(led, 1)

            elif self.__led_type == TYPE_LED:
                self.__led = Pin(self.__led_pin,Pin.OUT)

            else:
                raise StatusLedException("Unknown StatusLed type: %s" % self.__led_type)


    def on(self):
        if self.__led == None:
            return

        if self.__led_type == TYPE_NEOLED:
            self.__led.color(NEOLED_COLOR_ON)
        else:
            self.__led.value(1)


    def off(self):
        if self.__led == None:
            return

        if self.__led_type == TYPE_NEOLED:
            self.__led.color(NEOLED_COLOR_OFF)
        else:
            self.__led.value(0)
