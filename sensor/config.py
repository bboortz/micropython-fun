# 
# config
#
MY_STAGE = "test"
MY_LOCATION = "cellar-heating"
MY_HOST = "esp-sensor-" + MY_LOCATION + "-" + MY_STAGE
MY_MAC = "10aea47b97%s" % str(len(MY_HOST)),

CONFIG =	{
  # sensor types
  "ADC_SENSOR": False,
  "DHT11_SENSOR": False,
  "DHT22_SENSOR": False,
  "DS18X20_SENSOR": True,

  # pins
  "LED_PIN": 18,
  "TEMP_VORLAUF_PIN": 45,
  "TEMP_RUECKLAUF_PIN": 35,
  "SENSOR_VORLAUF_DHT22_PIN": 0, # anderes 4
  "SENSOR_RUECKLAUF_DHT22_PIN": 5,

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
      {
          "sensor_name": "vorlauf_temp",
          "sensor_type": "DS18X20_SENSOR",
          "sensor_pin": 45
      },
      {
          "sensor_name": "ruecklauf_temp",
          "sensor_type": "DS18X20_SENSOR",
          "sensor_pin": 42
      },
      {
          "sensor_name": "warmwasser_zirkulation_temp",
          "sensor_type": "DS18X20_SENSOR",
          "sensor_pin": 40
      }
  ]
}

