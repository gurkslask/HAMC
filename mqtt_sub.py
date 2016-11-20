"""Module for subscribing to mqtt topics."""
import paho.mqtt.client as mqtt
import json


def on_connect(client, userdata, flags, rc):
    """Subscribe on connect."""
    print(rc)
    client.subscribe('kgrund/fukt')
    client.subscribe('kgrund/temp')


def on_message(client, userdata, msg):
    """Callback on new message."""
    try:
        with open('mqtt_values.json', 'r') as f:
            json_data = json.loads(f)
    except FileNotFoundError as e:
        print('filenotfound, will create')
    json_data[msq.topic] = msg.payload
    with open('mqtt_values.json', 'w') as f:
        json.dumps(json_data, f)
    print(msg.topic + str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

if __name__ == '__main__':
    client.connect_async('192.168.1.8', 1883, 60)
    client.loop_forever()
