import paho.mqtt.client as mqtt
import time

import messageFormatter


def client():
    username = "project-software-engineering@ttn"
    password = "NNSXS.DTT4HTNBXEQDZ4QYU6SG73Q2OXCERCZ6574RVXI.CQE6IG6FYNJOO2MOFMXZVWZE4GXTCC2YXNQNFDLQL4APZMWU6ZGA"

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code " + str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe("extapi/data/esm")

    # The callback for when a PUBLISH message is received from the server.
    def on_message(client, userdata, msg):
        messageFormatter.formatMessage(msg.payload)

    def on_log(client, userdata, level, buf):
        print("log: ", buf)

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    # client.on_log = on_log
    client.username_pw_set(username, password)

    client.connect("eu1.cloud.thethings.network", 1883, 60)

    client.loop_start()
    client.subscribe("#")
    time.sleep(1000)

    client.loop_stop()
# client.loop_start()
#
# time.sleep(30)
# client.loop_stop()
