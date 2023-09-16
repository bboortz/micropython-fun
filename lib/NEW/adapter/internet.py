
try:
    from urllib.urequest import urlopen
except:
    from urllib.request import urlopen

from core.logger import Logger
from core.config import Config
from domain.networking import Networking, NetworkingException
from adapter.wifi_mock import WifiMock


#
# global constants
#
DEFAULT_CONNECTION = WifiMock()


#
# class
#

class Internet(Networking):

    def __init__(self, task_name = "setup_task", connection = DEFAULT_CONNECTION):
        self.connection = connection
        super().__init__(task_name)
        self.LOG.print_info("initialized")


    def is_connected(self) -> bool:
        if not self.connection.is_connected():
            return False

        connected = False
        i = 0
        max_retries = Config.get("INTERNET_CONNTEST_RETRIES")
        print(max_retries)
        while i < max_retries:
            try:
                urlopen(Config.get("INTERNET_CONNTEST_URL"), timeout=Config.get("INTERNET_CONNTEST_TIMEOUT"))
                self.LOG.print_debug("Connection Test succeeded!")
                connected = True
                break
            except:
                self.LOG.print_error("Connection Test failed!")
                connected = False
            finally:
                i += 1

        return connected


    def connect(self):
        self.connection.connect()
        self.is_connected()


    def disconnect(self, force=False):
        self.connection.disconnect()
