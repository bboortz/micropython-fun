PORT              ?= /dev/ttyUSB0
# BAUD_RATE         ?= 460800
# BAUD_RATE         ?= 230400
BAUD_RATE         ?= 115200
CHIP              ?= esp8266
CHIP_ESP8266       = esp8266
CHIP_ESP32         = esp32
CHIP_ESP32C3       = esp32c3
CHIP_ESP32C3S      = esp32c3s
CHIP_ESP32S2       = esp32s2
FIRMWARE_ESP8266   = esp8266-20230426-v1.20.0.bin 
FIRMWARE_ESP32     = esp32-20230426-v1.20.0.bin
FIRMWARE_ESP32C3   = firmware_generic_esp32_c3_2mb_1.18_4.3.1.bin # https://mega.nz/file/hFcRyQYa#yru2X7h9CxqwCrB_rDGKsZex_3y8dDfKxU-NtCCMWQg (https://forum.micropython.org/viewtopic.php?f=18&t=11025&sid=d9b90710278770df1b8f2c625cb4ddb3&start=10)
FIRMWARE_ESP32C3S  = esp32c3-usb-20230426-v1.20.0.bin
FIRMWARE_ESP32S2   = GENERIC_S2-20230426-v1.20.0.bin
SRC_FILES         := $(wildcard *.py)
OBJ_FILES         := $(patsubst %.py,%.pyc,$(SRC_FILES))


help:                     ## printing out the help
	@echo
	@echo micropython-fun Makefile
	@echo
	@echo --- TARGETS ---
	@grep -F -h "##" $(MAKEFILE_LIST) | grep -F -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'


bootstrap:                ## bootstrapping the virtualenv
	python -m venv .venv; \
	source .venv/bin/activate; \
	pip install -U -r requirements.txt; \
	mkdir -p lib/umqtt
	wget https://raw.githubusercontent.com/micropython/micropython-lib/master/micropython/umqtt.simple/umqtt/simple.py -O lib/umqtt/simple.py
	wget https://raw.githubusercontent.com/micropython/micropython-lib/master/micropython/umqtt.robust/umqtt/robust.py -O lib/umqtt/robust.py
	mkdir -p firmware
	wget https://micropython.org/resources/firmware/esp8266-20180511-v1.9.4.bin -O firmware/esp8266-20180511-v1.9.4.bin
	wget https://micropython.org/resources/firmware/esp8266-20190529-v1.11.bin -O firmware/esp8266-20190529-v1.11.bin
	wget https://micropython.org/resources/firmware/esp8266-20220618-v1.19.1.bin -O firmware/esp8266-20220618-v1.19.1.bin
	wget https://micropython.org/resources/firmware/esp8266-20230426-v1.20.0.bin -O firmware/esp8266-20230426-v1.20.0.bin
	wget https://micropython.org/resources/firmware/esp32-20220618-v1.19.1.bin -O firmware/esp32-20220618-v1.19.1.bin
	wget https://micropython.org/resources/firmware/esp32-20230426-v1.20.0.bin -O firmware/esp32-20230426-v1.20.0.bin
	wget https://micropython.org/resources/firmware/esp32c3-20220618-v1.19.1.bin -O firmware/esp32c3-20220618-v1.19.1.bin
	wget https://micropython.org/resources/firmware/esp32c3-20230426-v1.20.0.bin -O firmware/esp32c3-20230426-v1.20.0.bin
	wget https://micropython.org/resources/firmware/esp32c3-usb-20230426-v1.20.0.bin -O firmware/esp32c3-usb-20230426-v1.20.0.bin
	wget https://micropython.org/resources/firmware/GENERIC_S2-20220618-v1.19.1.bin -O firmware/GENERIC_S2-20220618-v1.19.1.bin
	wget https://micropython.org/resources/firmware/GENERIC_S2-20230426-v1.20.0.bin -O firmware/GENERIC_S2-20230426-v1.20.0.bin


cleanup:                  ## cleaning up the virtualenv
	rm -rf .venv


reset:                    ## soft-reset the board
	ampy -p $(PORT) -b $(BAUD_RATE) reset


abort:                    ## abort current program
	./tools/abort.py


get_flash_info:             ## retrieve the flash information
	esptool.py --chip $(CHIP) --port $(PORT) flash_id


erase_flash:              ## erasing the flash on device
	esptool.py --chip $(CHIP) --port $(PORT) --baud $(BAUD_RATE) erase_flash


flash:                    ## flashing the device with firmware
ifeq ($(CHIP),$(CHIP_ESP8266))
	esptool.py --port $(PORT) --baud 460800 write_flash --flash_size=detect 0 firmware/$(FIRMWARE_ESP8266)
else ifeq ($(CHIP),$(CHIP_ESP32))
	esptool.py --chip $(CHIP) --port $(PORT) write_flash -z 0x1000 firmware/$(FIRMWARE_ESP32)
else ifeq ($(CHIP),$(CHIP_ESP32C3))
	esptool.py --chip $(CHIP) --port $(PORT) write_flash -z 0x0 firmware/$(FIRMWARE_ESP32C3)
else ifeq ($(CHIP),$(CHIP_ESP32C3S))
	esptool.py --chip esp32c3 --port $(PORT) write_flash -z 0x0 firmware/$(FIRMWARE_ESP32C3S)
else ifeq ($(CHIP),$(CHIP_ESP32S2))
	esptool.py --chip $(CHIP) --port $(PORT) write_flash -z 0x1000 firmware/$(FIRMWARE_ESP32S2)
else
	echo "unknown chip!"
	exit 1
endif


monitor:                  ## monitor the devices using serial
	pyserial-miniterm $(PORT) $(BAUD_RATE)


get:                      ## retrieve boot code
	ampy -p $(PORT) -b $(BAUD_RATE) get boot.py


ls:                       ## retrieve boot code
	ampy -p $(PORT) -b $(BAUD_RATE) ls


put_libs:                 ## upload libraries
	ampy -p $(PORT) -b $(BAUD_RATE) mkdir --exists-okay lib
	ampy -p $(PORT) -b $(BAUD_RATE) put lib/device.py lib/device.py
	ampy -p $(PORT) -b $(BAUD_RATE) put lib/device_config.py lib/device_config.py
	ampy -p $(PORT) -b $(BAUD_RATE) put lib/logger.py lib/logger.py
	ampy -p $(PORT) -b $(BAUD_RATE) put lib/status_led.py lib/status_led.py
	ampy -p $(PORT) -b $(BAUD_RATE) put lib/events.py lib/events.py
	ampy -p $(PORT) -b $(BAUD_RATE) put lib/wifi.py lib/wifi.py
	ampy -p $(PORT) -b $(BAUD_RATE) put lib/mqtt.py lib/mqtt.py
	ampy -p $(PORT) -b $(BAUD_RATE) put lib/ntptime.py lib/ntptime.py
	ampy -p $(PORT) -b $(BAUD_RATE) put lib/neoled.py lib/neoled.py
	ampy -p $(PORT) -b $(BAUD_RATE) put lib/sensors.py lib/sensors.py
	ampy -p $(PORT) -b $(BAUD_RATE) put lib/temp.py lib/temp.py
	ampy -p $(PORT) -b $(BAUD_RATE) put lib/humi.py lib/humi.py
	ampy -p $(PORT) -b $(BAUD_RATE) put lib/watchdogtimer.py lib/watchdogtimer.py
	ampy -p $(PORT) -b $(BAUD_RATE) mkdir --exists-okay lib/umqtt
	ampy -p $(PORT) -b $(BAUD_RATE) put lib/umqtt/simple.py lib/umqtt/simple.py
	ampy -p $(PORT) -b $(BAUD_RATE) put lib/umqtt/robust.py lib/umqtt/robust.py
	ampy -p $(PORT) -b $(BAUD_RATE) put boot.py boot.py
#	ampy -p $(PORT) -b $(BAUD_RATE) put lib/http_timeouts.py lib/http_timeouts.py
#	ampy -p $(PORT) -b $(BAUD_RATE) put lib/http_requests.py lib/http_requests.py
#	ampy -p $(PORT) -b $(BAUD_RATE) put lib/http_webserver.py lib/http_webserver.py


put: $(OBJ_FILES)         ## upload software
	@echo "software uploaded"


mosquitto:                ## start mosquitto server
	mosquitto -c mosquitto/mosquitto.conf -v


%.pyc: %.py
	ampy -p $(PORT) -b $(BAUD_RATE) put $< $<

