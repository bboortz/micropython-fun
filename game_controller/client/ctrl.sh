#!/bin/bash

set -e
set -u


xdotool search --onlyvisible --class gedit windowactivate
sleep 0.5
xdotool key k Return j Page_Up Page_Down Left Return
xdotool keydown a
sleep 1
xdotool keyup a
