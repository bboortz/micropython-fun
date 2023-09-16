
import time
try:
    import uasyncio as asyncio
except:
    import asyncio

from core.logger import Logger
from core.config import Config
from domain.networking import Networking


#
# class
#
class WifiMock(Networking):

    def __init__(self, task_name = "setup_task", client_host = "localhost-test", client_mac = "00:11:22:AA:BB:CC", wifi_ssid = "wifi-test", wifi_pass = "wifi-pass"):
        self.client_host = client_host
        self.client_mac = client_mac
        self.wifi_ssid = wifi_ssid
        self.wifi_pass = wifi_pass
        super().__init__(task_name)
        self.LOG.print_info("initialized")


    def is_connected(self) -> bool:
        return True


    def connect(self):
        self.LOG.print_cmd('Connecting to Wifi: {}'.format(self.wifi_ssid))
        self.activate()
        self.set_hostname(self.client_host)
        self.set_mac(self.client_mac)
        self.LOG.print_info('Connected to Wifi: {}'.format(self.wifi_ssid))
        self.info()


    def disconnect(self, force=False):
        self.LOG.print_cmd('Disconnecting from Wifi: {}'.format(self.wifi_ssid))
        self.LOG.print_info('Disconnected from Wifi: {}'.format(self.wifi_ssid))


    def info(self):
        if self.is_connected():
            self.LOG.print_info('** Wifi Info **')
            self.LOG.print_info('  Wifi ESSID: {}'.format( self.wifi_ssid ))
            self.LOG.print_info('  Network config: 127.0.0.1')
            self.LOG.print_info('  Mac: {}'.format(self.client_mac))


    def set_mac(self, mac):
        self.LOG.print_cmd('Set MAC to {}'.format(mac))


    def set_hostname(self, host):
        self.LOG.print_cmd('Set Hostname to: {}'.format(self.client_host))


    async def activate(self):
        self.LOG.print_info('NIC activated!')
        await asyncio.sleep( Config.get("WIFI_ACTIVATE_WAIT_MS") / 1000 )


    async def deactivate(self):
        self.LOG.print_info('NIC deactivated!')
        await asyncio.sleep( Config.get("WIFI_ACTIVATE_WAIT_MS") / 1000 )
        
