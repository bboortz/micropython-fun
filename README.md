# micropython-fun

Some simple micropython projects I build just for fun. Tested on this hardware
* ESP8266
* EPS34



## Projects

* [Sensor](sensor/) - temperature and humidity sensor
* [WebServer](webserver/) - simple webserver
* [Wifi Scan](wifi_scan/) - simple wifi scanner
* [Game Controller](game_controller/) - a game controller that sends commands via mqtt



## Lib

The projects are using some python files from [lib](lib/) directory.


## Firmware

The used firmware will be downloaded from https://micropython.org/download/ and stored to the [firmware](firmware/) directory.

## Usage


### Help

```
make help
```


### Bootstrapping the local environment

```
make bootstrap
source .venv/bin/activate
```


### Flashing Device


#### ESP8266

```
make erase_flash CHIP=esp8266
make flash CHIP=esp8266
```


### Building and pushing software

For example to build and push the sensor project:

```
make put_libs
cd sensor
cat << EOF > secrets.py
WIFI_SSID = 'YOURWIFISSID'¬
WIFI_PASS = 'YOURWIFIPASS'¬
EOF
make put
```


### Monitor the device via serial interface / usb

```
make monitor
```

