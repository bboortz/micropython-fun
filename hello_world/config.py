# 
# config
#
from device_config import MACHINE_ID_QSUM


MY_STAGE = "test"
MY_LOCATION = "cellar-heating"
MY_HOST = "esp-sensor-" + MY_LOCATION + "-" + MY_STAGE + str( MACHINE_ID_QSUM )

MY_STAGE_HEX = "{0:02x}".format(ord( MY_STAGE[0] ))
MY_LOCATION_HEX = "{0:02x}".format(ord( MY_LOCATION[0] ))
MY_HOST_LEN = str(len(MY_HOST))
MY_MAC = "2222%s%s%s%s" % (MY_STAGE_HEX, MY_LOCATION_HEX, MY_HOST_LEN, MACHINE_ID_QSUM)


CONFIG =	{
  # events
  "EVENTS_FILE": "events.csv",

  # pins
  "STATUS_LED":  {
          "TYPE": "LED",
          "PIN": 2
  },

  # location
  "MY_STAGE": MY_STAGE,
  "MY_LOCATION": MY_LOCATION,
  "MY_HOST": MY_HOST,
  "MY_MAC": MY_MAC,

  # mqtt
  "MQTT_BROKER": "mosquitto.pub-a.devara.world",
  "MQTT_CLIENT_NAME": MY_HOST,
  "MQTT_TOPIC": "sensornet/measurements",
  "MQTT_TOPIC_EVENTS": "sensornet/events",

  # intervals & timeouts
  "BOOT_WAIT_MS": 1000,
  "HELLO_INTERVAL_MS": 1000,
  "WDT_TIMEOUT_MS": 3000,

  "SENSORS":
  [
  ]
}

