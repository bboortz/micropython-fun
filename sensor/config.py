# 
# config
#
from device import MACHINE_ID_QSUM


MY_STAGE = "dev"
MY_LOCATION = "living-room"
MY_HOST = "esp-sensor-" + MY_LOCATION + "-" + MY_STAGE + "-" + str( MACHINE_ID_QSUM )

MY_STAGE_HEX = "{0:02x}".format(ord( MY_STAGE[0] ))
MY_LOCATION_HEX = "{0:02x}".format(ord( MY_LOCATION[0] ))
MY_HOST_LEN = str(len(MY_HOST))
MY_MAC = "2222%s%s%s%s" % (MY_STAGE_HEX, MY_LOCATION_HEX, MY_HOST_LEN, MACHINE_ID_QSUM)


CONFIG =	{
  # pins
  "LED_PIN": 18,

  # location
  "MY_STAGE": MY_STAGE,
  "MY_LOCATION": MY_LOCATION,
  "MY_HOST": MY_HOST,
  "MY_MAC": MY_MAC,

  # mqtt
  "MQTT_BROKER": "mosquitto.pub-a.devara.world",
  "MQTT_CLIENT_NAME": MY_HOST,
  "MQTT_TOPIC": "sensornet/measurements",

  # intervals & timeouts
  "BOOT_WAIT_MS": 3000,
  "MEASUREMENT_INTERVAL_MS": 5000,
  "PUBLISH_INTERVAL_MS": 5000,
  "PUBLISH_TIMEOUT_MS": 5000,

  "SENSORS":
  [
#      {
#          "sensor_name": "heizkoerper_vorlauf_temp",
#          "sensor_type": "DS18X20_SENSOR",
#          "sensor_pin": 45
#      },
#      {
#          "sensor_name": "raum_temp",
#          "sensor_type": "DHT22_SENSOR",
#          "sensor_pin": 42
#      }
  ]
}

