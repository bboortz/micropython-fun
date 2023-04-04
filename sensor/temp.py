from config import CONFIG

import time
import logger
from machine import Pin

if CONFIG.get("DHT11_SENSOR"):
    import dht
elif CONFIG.get("DHT22_SENSOR"):
    import dht
elif CONFIG.get("DS18X20_SENSOR"):
    import onewire, ds18x20
else:
    logger.print_error("Configuration broken! Cannot load imports!")
    

class TempSensor:

    def __init__(self, sensor_type, pin, wait_interval_ms):
        self.sensor_type = sensor_type
        self.pin = pin
        self.wait_interval_ms = wait_interval_ms
        self.last_measure_time = 0
        self.last_measure_temp = 0


    def setup_sensor(self):
        if self.sensor_type == "DHT11_SENSOR":
            self.sensor = dht.DHT11(machine.Pin(self.pin))
        elif self.sensor_type == "DHT22_SENSOR":
            self.sensor = dht.DHT11(machine.Pin(self.pin))
        elif self.sensor_type == "DS18X20_SENSOR":
            ds = ds18x20.DS18X20(onewire.OneWire(self.pin))
            roms = ds.scan()
            self.rom = roms[0]
            print('found DS18X20 devices:', roms)
            ds.convert_temp()
            self.sensor = ds
        else:
            logger.print_error("Wrong sensor_type!")


    def measure(self):
        # dont measure faster than wait_interval_ms
        time_diff = time.ticks_ms() - self.last_measure_time
        if time_diff < self.wait_interval_ms:
            logger.print_info("using cached measurement")
            return self.last_measure_temp

        if self.sensor_type == "DHT11_SENSOR":
            self.sensor.measure()
            self.last_measure_temp = self.sensor.temperature()
            self.last_measure_time = time.ticks_ms()
            return self.last_measure_temp
        elif self.sensor_type == "DHT22_SENSOR":
            self.measure()
            self.last_measure_temp = self.sensor.temperature()
            self.last_measure_time = time.ticks_ms()
            return self.last_measure_temp
        elif self.sensor_type == "DS18X20_SENSOR":
            self.last_measure_temp = self.sensor.read_temp(self.rom)
            self.last_measure_time = time.ticks_ms()
            return self.last_measure_temp
        else:
            logger.print_error("Wrong sensor_type!")

    def init_next_measure(self):
        if self.sensor_type == "DHT11_SENSOR":
            pass
        elif self.sensor_type == "DHT22_SENSOR":
            pass
        elif self.sensor_type == "DS18X20_SENSOR":
            self.sensor.convert_temp()
        else:
            logger.print_error("Wrong sensor_type!")
