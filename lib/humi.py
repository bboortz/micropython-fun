from config import CONFIG

import sys
import time
import logger


class HumiSensorException(BaseException):
    pass


class HumiSensor:

    def __init__(self, sensor_type, pin, wait_interval_ms):
        self.sensor_type = sensor_type
        self.pin = pin
        self.wait_interval_ms = wait_interval_ms
        self.last_measure_time = 0
        self.last_measure_humi = 0


    def setup_sensor(self):
        logger.print_cmd("setting up sensor: (%s, %s)" % (self.sensor_type, self.pin) )

        try:
            if self.sensor_type == "DHT11_SENSOR":
                import dht
                self.sensor = dht.DHT11(self.pin)
            elif self.sensor_type == "DHT22_SENSOR":
                import dht
                self.sensor = dht.DHT22(self.pin)
            else:
                logger.print_error("Wrong sensor_type!")
                raise HumiSensorException("Wrong sensor_type")

        except Exception as e:
            logger.print_error("Sensor not found!")
            raise(e)


    def measure(self):
        # dont measure faster than wait_interval_ms
        time_diff = time.ticks_ms() - self.last_measure_time
        if time_diff < self.wait_interval_ms:
            logger.print_info("using cached measurement")
            return self.last_measure_humi

        if self.sensor_type == "DHT11_SENSOR":
            self.sensor.measure()
            self.last_measure_humi = self.sensor.humidity()
            self.last_measure_time = time.ticks_ms()
            return self.last_measure_humi
        elif self.sensor_type == "DHT22_SENSOR":
            self.sensor.measure()
            self.last_measure_humi = self.sensor.humidity()
            self.last_measure_time = time.ticks_ms()
            return self.last_measure_humi
        else:
            logger.print_error("Wrong sensor_type!")
            raise HumiSensorException("Wrong sensor_type")


    def init_next_measure(self):
        if self.sensor_type == "DHT11_SENSOR":
            pass
        elif self.sensor_type == "DHT22_SENSOR":
            pass
        else:
            logger.print_error("Wrong sensor_type!")
            raise HumiSensorException("Wrong sensor_type")


    def get_unit(self):
        return "%"
