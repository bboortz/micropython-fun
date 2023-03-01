PORT              ?= /dev/ttyUSB0
CHIP              ?= esp8266
CHIP_ESP8266       = esp8266
CHIP_ESP32         = esp32
FIRMWARE_ESP8266   = esp8266-20220618-v1.19.1.bin
FIRMWARE_ESP32     = esp32-20220618-v1.19.1.bin
SRC_FILES         := $(wildcard *.py)
OBJ_FILES         := $(patsubst %.py,%.pyc,$(SRC_FILES))


help:                     ## printing out the help
	@echo
	@echo micropython-fun Makefile
	@echo
	@echo --- TARGETS ---
	@grep -F -h "##" $(MAKEFILE_LIST) | grep -F -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'


bootstrap:                ## bootstrapping the virtualenv
	virtualenv .venv; \
	source .venv/bin/activate; \
	pip install -U -r requirements.txt; \
	mkdir -p lib/umqtt
	wget https://raw.githubusercontent.com/micropython/micropython-lib/master/micropython/umqtt.simple/umqtt/simple.py -O lib/umqtt/simple.py
	wget https://raw.githubusercontent.com/micropython/micropython-lib/master/micropython/umqtt.robust/umqtt/robust.py -O lib/umqtt/robust.py
	mkdir -p firmware
	wget https://micropython.org/resources/firmware/esp8266-20180511-v1.9.4.bin -O firmware/esp8266-20180511-v1.9.4.bin
	wget https://micropython.org/resources/firmware/esp8266-20190529-v1.11.bin -O firmware/esp8266-20190529-v1.11.bin
	wget https://micropython.org/resources/firmware/esp8266-20220618-v1.19.1.bin -O firmware/esp8266-20220618-v1.19.1.bin
	wget https://micropython.org/resources/firmware/esp32-20220618-v1.19.1.bin -O firmware/esp32-20220618-v1.19.1.bin


cleanup:                  ## cleaning up the virtualenv
	rm -rf .venv


erase_flash:              ## erasing the flash on device
	esptool.py --chip $(CHIP) -p $(PORT) erase_flash


flash:                    ## flashing the device with firmware
ifeq ($(CHIP),$(CHIP_ESP8266))
	esptool.py -p $(PORT) --baud 460800 write_flash --flash_size=detect 0 firmware/$(FIRMWARE_ESP8266)
else
	esptool.py --chip $(CHIP) -p $(PORT) write_flash -z 0x1000 firmware/$(FIRMWARE_ESP32)
endif


monitor:                  ## monitor the devices using serial
	pyserial-miniterm /dev/ttyUSB0 115200


get:                      ## retrieve boot code
	ampy -p /dev/ttyUSB0 -b 115200 get boot.py


put_libs:                 ## upload libraries
	ampy -p /dev/ttyUSB0 -b 115200 mkdir --exists-okay lib
	ampy -p /dev/ttyUSB0 -b 115200 put lib/logger.py lib/logger.py
	ampy -p /dev/ttyUSB0 -b 115200 put lib/wifi.py lib/wifi.py
	ampy -p /dev/ttyUSB0 -b 115200 put lib/mqtt.py lib/mqtt.py
	ampy -p /dev/ttyUSB0 -b 115200 mkdir --exists-okay lib/umqtt
	ampy -p /dev/ttyUSB0 -b 115200 put lib/umqtt/simple.py lib/umqtt/simple.py
	ampy -p /dev/ttyUSB0 -b 115200 put lib/umqtt/robust.py lib/umqtt/robust.py
#	ampy -p /dev/ttyUSB0 -b 115200 put lib/http_timeouts.py lib/http_timeouts.py
#	ampy -p /dev/ttyUSB0 -b 115200 put lib/http_requests.py lib/http_requests.py
#	ampy -p /dev/ttyUSB0 -b 115200 put lib/http_webserver.py lib/http_webserver.py


put: $(OBJ_FILES)         ## upload software
	@echo "software uploaded"


mosquitto:                ## start mosquitto server
	mosquitto -c mosquitto/mosquitto.conf -v


%.pyc: %.py
	ampy -p /dev/ttyUSB0 -b 115200 put $< $<

