from config import CONFIG

import sys
import time
import logger


class SensorException(BaseException):
    pass


class TempSensor:

    def __init__(self, sensor_type, pin, wait_interval_ms):
        self.sensor_type = sensor_type
        self.pin = pin
        self.wait_interval_ms = wait_interval_ms
        self.last_measure_time = 0
        self.last_measure_temp = 0


    def setup_sensor(self):
        try:
            if self.sensor_type == "DHT11_SENSOR":
                import dht
                self.sensor = dht.DHT11(self.pin)
            elif self.sensor_type == "DHT22_SENSOR":
                import dht
                self.sensor = dht.DHT22(self.pin)
            elif self.sensor_type == "DS18X20_SENSOR":
                import onewire, ds18x20
                ds = ds18x20.DS18X20(onewire.OneWire(self.pin))
                roms = ds.scan()
                try:
                    self.rom = roms[0]
                except Exception as e:
                    logger.print_error("Sensor not found!")
                    print(e)
                    raise()

                print('found DS18X20 devices:', roms)
                ds.convert_temp()
                self.sensor = ds
            else:
                logger.print_error("Wrong sensor_type!")
                raise SensorException("Wrong sensor_type")

        except Exception as e:
            logger.print_error("Sensor not found!")
            print(e)
            raise()


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
            self.sensor.measure()
            self.last_measure_temp = self.sensor.temperature()
            self.last_measure_time = time.ticks_ms()
            return self.last_measure_temp
        elif self.sensor_type == "DS18X20_SENSOR":
            self.last_measure_temp = self.sensor.read_temp(self.rom)
            self.last_measure_time = time.ticks_ms()
            return self.last_measure_temp
        else:
            logger.print_error("Wrong sensor_type!")
            raise SensorException("Wrong sensor_type")


    def init_next_measure(self):
        if self.sensor_type == "DHT11_SENSOR":
            pass
        elif self.sensor_type == "DHT22_SENSOR":
            pass
        elif self.sensor_type == "DS18X20_SENSOR":
            self.sensor.convert_temp()
        else:
            logger.print_error("Wrong sensor_type!")
            raise SensorException("Wrong sensor_type")
