import paho.mqtt.client as mqtt
from time import sleep

"""def on_connect(client, userdata, flags, rc):
    print(rc)
    client.publish("kgrund/fukt", 42)

def on_message(client, userdata, msg):
    print(msg.topic + str(msg.payload))"""

client = mqtt.Client()
"""client.on_connect = on_connect
client.on_message = on_message"""

client.connect('192.168.1.8', 1883, 60)
client.loop_start()
i = 0

while True:
    client.publish("kgrund/fukt", i)
    i += 1
    sleep(1)

