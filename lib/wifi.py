import logger
import time
import network
import ubinascii

# 
# global constants
#
MAX_RETIRES = 20


#
# class
#
class WifiException(BaseException):
    pass


class Wifi:

    def __init__(self, wdt):
        self.__nic = network.WLAN(network.STA_IF)
        self.__wdt = wdt
        self.deactivate()


    def do_connect(self, host, mac, wifi_ssid, wifi_pass):
        self.activate()
        self.set_hostname(host)
        self.set_mac(mac)
        self.connect(wifi_ssid, wifi_pass)
        self.info()


    def is_connected(self):
        logger.print_cmd('Test WIFI Connection')
        ret = self.__nic.isconnected()

        if not ret:
            logger.print_info('Wifi Disconnected!')
        else:
            logger.print_info('Wifi Connected!')

        return ret


    def connect(self, ssid, password):
        retries = 0
        if not self.is_connected():
            logger.print_cmd('Connect to Wifi {}'.format(ssid))
            self.__nic.connect(ssid, password)
            while not self.__nic.isconnected():
                self.__wdt.feed()
                retries +=1
                if retries > MAX_RETIRES:
                    raise WifiException("The wifi connect retries has exceeded the MAX_RETIRES(%d)" % retries)
                time.sleep_ms(1000)
                logger.print_wait()
                #print(self.__nic.ifconfig())



    def disconnect(self):
        logger.print_cmd('Disconnect from Wifi')
        self.__nic.disconnect()


    def info(self):
        if self.is_connected():
            logger.print_info('Wifi ESSID: {}'.format( self.__nic.config('essid') ))
            logger.print_info('Network config: {}'.format( self.__nic.ifconfig() ))
            mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
            logger.print_info('Mac: {}'.format(mac))


    def set_mac(self, mac):
        logger.print_cmd('Set MAC to {}'.format(mac))

        emac = mac.encode()
        bmac = ubinascii.unhexlify(emac)
        self.__nic.config(mac=bmac)


    def set_hostname(self, host):
        logger.print_cmd('Set Hostname to {}'.format(host))
        network.hostname(host)
#        self.__nic.config(dhcp_hostname=host) # old variant

    def scan_ssids(self):
        return self.__nic.scan()

    def activate(self):
        self.__nic.active(True)
        logger.print_info('NIC activated: {}'.format(self.__nic.active()))
        time.sleep_ms(1000)

    def deactivate(self):
        self.__nic.active(False)
        logger.print_info('NIC activated: {}'.format(self.__nic.active()))
        time.sleep_ms(1000)
