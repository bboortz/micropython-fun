# micropython-fun

Some simple micropython projects I build just for fun. Tested on this hardware
* ESP8266
* EPS32
* EPS32C3



## Projects

* [Sensor](sensor/) - temperature and humidity sensor
* [WebServer](webserver/) - simple webserver
* [Wifi Scan](wifi_scan/) - simple wifi scanner
* [Game Controller](game_controller/) - a game controller that sends commands via mqtt



## Lib

The projects are using some python files from [lib](lib/) directory.


## Firmware

The used firmware will be downloaded from https://micropython.org/download/ and stored to the [firmware](firmware/) directory.

## Building own Firmware

official documentation: https://github.com/micropython/micropython/blob/master/ports/esp32/README.md
workflow:
```
git clone -b v4.4.5 --recursive https://github.com/espressif/esp-idf.git esp-idf-v4.4.5
git clone -b v1.20.0 --recursive https://github.com/micropython/micropython.git/ micropython-v1.2.0
cd esp-idf-v4.4.5
./install.sh
cd ../micropython-v1.2.0
. ../esp-idf-v4.4.5/export.sh # as a zsh user: switch to bash in beforehand
vim py/stackctrl.h # fix https://github.com/orgs/micropython/discussions/12027
make -C mpy-cross
cd ports/esp32/
make submodules
cp -r boards/GENERIC_C3 boards/GENERIC_C3_2MB
vim boards/GENERIC_C3_2MB/sdkconfig.board # copy values from the files from https://forum.micropython.org/viewtopic.php?f=18&t=11025
vim boards/GENERIC_C3_2MB/mpconfigboard.cmake # add line "boards/GENERIC_C3_2MB/sdkconfig.board"
make BOARD=GENERIC_C3_2MB
du -shc build-GENERIC_C3_2MB/firmware.bin
esptool.py --chip esp32c3 --port /dev/ttyUSB0 write_flash -z 0x0 build-GENERIC_C3_2MB/firmware.bin
```

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

