import temp

import time
import logger
from machine import Pin


def get_sensors(config):
    sensors_dict = config.get("SENSORS")
    measurement_interval_ms = config.get("MEASUREMENT_INTERVAL_MS")
    sensors = []

    for s in sensors_dict:  
        s_name = s.get("sensor_name")
        s_pin = s.get("sensor_pin")
        s_sensor = temp.TempSensor(s.get("sensor_type"), Pin(s_pin), measurement_interval_ms)
        s_sensor.setup_sensor()
        s_dict = {
                "name": s_name,
                "pin": s_pin,
                "sensor": s_sensor,
        }
        sensors.append(s_dict)

    print("sensors: %s" % sensors)
    return sensors
