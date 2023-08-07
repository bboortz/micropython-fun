from machine import WDT
import logger

# 
# global constants
#
DEFAULT_WDT_MS = 5000 #ms
MAX_WDT_MS = 8000 #ms


#
# class
#
class WatchdogTimerException(BaseException):
    pass


class WatchdogTimer:

    def __init__(self, wdt_timeout = DEFAULT_WDT_MS):
        if wdt_timeout > MAX_WDT_MS:
            raise WatchdogTimerException("wdt_timeout(%d) is greater than MAX_WDT_MS(%d). Reduce wdt_timeout to lower or equal of MAX_WDT_MS." % (wdt_timeout, MAX_WDT_MS) )

        self.__wdt_timeout = wdt_timeout
        try:
            self.__wdt = WDT(timeout = wdt_timeout)
        except:
            self.__wdt = WDT()
        self.__wdt.feed()
        logger.print_info("WDT activiated")


    def feed(self):
        self.__wdt.feed()
