PORT              ?= /dev/ttyUSB0
CHIP              ?= esp8266
CHIP_ESP8266       = esp8266
CHIP_ESP32         = esp32
FIRMWARE_ESP8266   = esp8266-20180511-v1.9.4.bin
FIRMWARE_ESP32     = esp32-20190112-v1.9.4-779-g5064df207.bin
SRC_FILES         := $(wildcard *.py)
OBJ_FILES         := $(patsubst %.py,%.pyc,$(SRC_FILES))


help:                     ## printing out the help
	@echo
	@echo micropython-test Makefile
	@echo
	@echo --- TARGETS ---
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'


bootstrap:                ## bootstrapping the virtualenv
	virtualenv .venv; \
	source .venv/bin/activate; \
	pip install -U -r requirements.txt; \
	mkdir -p lib/umqtt
	wget https://raw.githubusercontent.com/micropython/micropython-lib/master/umqtt.simple/umqtt/simple.py -O lib/umqtt/simple.py
	mkdir -p firmware
	wget http://micropython.org/resources/firmware/esp8266-20180511-v1.9.4.bin -O firmware/esp8266-20180511-v1.9.4.bin
	wget http://micropython.org/resources/firmware/esp32-20190112-v1.9.4-779-g5064df207.bin -O firmware/esp32-20190112-v1.9.4-779-g5064df207.bin


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
	miniterm.py /dev/ttyUSB0 115200


get:                      ## retrieve boot code
	ampy -p /dev/ttyUSB0 -b 115200 get boot.py


put_libs:                 ## upload libraries
	ampy -p /dev/ttyUSB0 -b 115200 mkdir --exists-okay lib
	ampy -p /dev/ttyUSB0 -b 115200 put lib/logger.py lib/logger.py
	ampy -p /dev/ttyUSB0 -b 115200 put lib/wifi.py lib/wifi.py
	ampy -p /dev/ttyUSB0 -b 115200 put lib/mqtt.py lib/mqtt.py
	ampy -p /dev/ttyUSB0 -b 115200 mkdir --exists-okay lib/umqtt
	ampy -p /dev/ttyUSB0 -b 115200 put lib/umqtt/simple.py lib/umqtt/simple.py
#	ampy -p /dev/ttyUSB0 -b 115200 put lib/http_timeouts.py lib/http_timeouts.py
#	ampy -p /dev/ttyUSB0 -b 115200 put lib/http_requests.py lib/http_requests.py
#	ampy -p /dev/ttyUSB0 -b 115200 put lib/http_webserver.py lib/http_webserver.py


put: $(OBJ_FILES)         ## upload software
	@echo "software uploaded"


%.pyc: %.py
	ampy -p /dev/ttyUSB0 -b 115200 put $< $<

