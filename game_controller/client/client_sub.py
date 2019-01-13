#!/usr/bin/env python

import paho.mqtt.client as mqtt
from subprocess import call

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))

	# Subscribing in on_connect() means that if we lose the connection and
	# reconnect then subscriptions will be renewed.
	client.subscribe("game/game-controller/control")

	call(["xdotool", "search", "--onlyvisible", "--class", "chromium-bsu", "windowactivate"])


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	print(msg.payload)
	if msg.payload == b'A':
		call(["xdotool", "key", "space"])
	elif msg.payload == b'B':
		call(["xdotool", "key", "Return"])
	elif msg.payload == b'L':
		call(["xdotool", "key", "Left"])
	elif msg.payload == b'R':
		call(["xdotool", "key", "Right"])
	elif msg.payload == b'U':
		call(["xdotool", "key", "Up"])
	elif msg.payload == b'D':
		call(["xdotool", "key", "Down"])

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
