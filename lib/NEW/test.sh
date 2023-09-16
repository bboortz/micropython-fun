#!/bin/bash

set -e # react on exit != 0
set -u # exit on unassigned variables
set -m # job control

MOSQUITTO_CONF=$( readlink -f ../../mosquitto/mosquitto.conf )
LOG_OUT="> /dev/null 2>&1"
#LOG_OUT=""


exit_trap() {
  echo
  stop_mosquitto || true
  echo "EXIT: $?"
  echo
}
trap exit_trap EXIT


run_test() {
  local cmd="$1"
  echo
  echo "********************************************"
  echo "*** TEST: $cmd"
  stop_mosquitto || true
  eval $cmd $LOG_OUT
  echo RESULT: $?
  stop_mosquitto || true
  echo
}


start_mosquitto() {
  docker run --name mosquitto-dev --detach -p 1883:1883 -p 9001:9001 --rm -v ${MOSQUITTO_CONF}:/mosquitto/config/mosquitto.conf eclipse-mosquitto
  sleep 0.3
}

stop_mosquitto() {
  eval docker stop mosquitto-dev $LOG_OUT
}

run_mock_test() {
  ./tests/run_mock.py
}

run_normal() {
  start_mosquitto
  ./tests/run_setup_check.py
  ./tests/run_health_check.py
  stop_mosquitto
}

run_restart() {
  start_mosquitto
  ./tests/run_health_check.py &
  sleep 0.5
  stop_mosquitto
  sleep 1
  start_mosquitto
  fg %1
  stop_mosquitto
}

run_late_mosquitto_start() {
  ./tests/run_health_check.py &
  start_mosquitto
  fg %1
  stop_mosquitto
}


stop_mosquitto || true
run_test run_mock_test
run_test run_normal
run_test run_late_mosquitto_start
run_test run_restart
