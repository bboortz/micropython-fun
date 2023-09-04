
print('\n\n')
print("--------------------- RUN PROGRAM ---------------------")



#
# import
# 
import sys
import time
import uasyncio as asyncio
import ujson as json
from config import CONFIG
import temp
import logger



# 
# global constants
#
MQTT_TOPIC_MEASUREMENTS = CONFIG.get("MQTT_TOPIC_MEASUREMENTS")

MEASUREMENT_INTERVAL_MS  = CONFIG.get("MEASUREMENT_INTERVAL_MS")
DEEPSLEEP_MS = CONFIG.get("DEEPSLEEP_MS")

health_t = None



#
# functions
#
def measure(mqtt, counter, sensors, topic):
    try:
        t = time.localtime()
        datetime = "%4d-%02d-%02dT%02d:%02d:%02d.000Z" % (t[0], t[1], t[2], t[3], t[4], t[5])
        ticks_s = int(time.ticks_ms() / 1000)

        json_data = { 
            "stage": MY_STAGE, 
            "location": MY_LOCATION,
            "device": MY_HOST,
            "measure_count": counter, 
            "datetime": datetime,
            "ticks_s": ticks_s,
        }

        for s in sensors:
            name = s.get("name")
            sensor = s.get("sensor")
            sensor_res = sensor.measure()
            sensor.init_next_measure()
            u = sensor.get_unit()
            json_data.update({name: sensor_res})
            print("Result: %3.3f %s" % (sensor_res, u))

        json_str = json.dumps(json_data)
        print(json_str)
        mqtt.publish(topic, json_str)
    except Exception as e:
        EVENTS.event("error", "Measurement failed: %s" % getattr(e, 'message', repr(e)) )
        program_state.err_counter += 1
        if program_state.err_counter > program_state.max_errors:
            EVENTS.event("error", "initiating soft reset because program_state.err_counter is reaching program_state.max_errors.")
            EVENTS.soft_reset()



#
# tasks
#
async def health_task():
    while True:
        wait_ms = MEASUREMENT_INTERVAL_MS * 5
        await asyncio.sleep_ms(wait_ms)

        if program_state.is_stopped():
            EVENTS.event("info", "task health_task stopped!")
            break
        if not program_state.is_setup_done():
            continue

        try:
            program_state.mqtt.ping()
            program_state.set_state_healthy()
        except Exception as e:
            logger.print_error("UNHEALTHY")
            program_state.set_state_unhealthy()
            program_state.mqtt.disconnect()
            program_state.wifi.disconnect()
            program_state.mqtt = None
            program_state.wifi = None


async def measure_task():
    # loop for measuring and publishing data
    while True:
        program_state.wdt.feed()
        await asyncio.sleep_ms(MEASUREMENT_INTERVAL_MS)
        program_state.wdt.feed()

        if program_state.is_stopped():
            EVENTS.event("info", "task measure_task stopped!")
            break
        if not program_state.is_setup_done():
            continue

        if program_state.counter > program_state.max_counter:
            EVENTS.event("error", "initiating soft reset because program_state.counter is reaching program_state.max_counter.")
            EVENTS.soft_reset()

        print("----------- MEASURE AND PUBLISH: %d -----------" % program_state.counter)
        program_state.led.on()

        if len(program_state.sensors) == 0:
            logger.print_info("no sensors configured.")
        else:
            measure(program_state.mqtt, program_state.counter, program_state.sensors, MQTT_TOPIC_MEASUREMENTS)

        program_state.led.off()
        program_state.counter += 1


async def main():
    global health_t

    EVENTS.event("info", "main() function running ...", program_state.counter)
    await asyncio.sleep_ms(BOOT_WAIT_MS)

    EVENTS.event("info", "Starting tasks ...", program_state.counter)
    health_t = tasks.create_task("health_task", health_task())
    measure_t = tasks.create_task("measure_task", measure_task())
    await asyncio.gather(health_t, measure_t)



while True:
    try:
        # uncomment for testing the exception handling
        #from events import EventsException
        #raise EventsException("aaa")
        asyncio.run(main())
    except KeyboardInterrupt:
        EVENTS.event("error", "Ctrl-C", program_state.counter)
        health_t.cancel()
        health_t = None
    except Exception as e:
        EVENTS.event("error", "Failed in main() function because of an Exception!", program_state.counter)
        sys.print_exception(e)
        EVENTS.soft_reset()
    except:
        EVENTS.event("error", "Failed in main() function because of an *UNCATCHED* Exception!", program_state.counter)
        EVENTS.soft_reset()
