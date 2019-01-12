# micropython-fun

Some simple micropython projects I build just for fun. Tested on this hardware
* ESP8266
* EPS34



## Projects

* [Sensor](sensor/) - temperature and humidity sensor
* [WebServer](webserver/) - simple webserver



## Lib

The projects are using some python files from [lib](lib/) directory.



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

