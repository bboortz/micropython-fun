#!/bin/bash

set -e
set -u


xdotool search --onlyvisible --class gedit windowactivate
sleep 0.5
xdotool key k Return j Page_Up Page_Down Left Return
