"""Reads temperature and humidity from a DHT11 with a ESP8266 via MQTT."""
from machine import Pin
from dht import DHT11
import time
import ubinascii
from umqtt.simple import MQTTClient

d = DHT11(Pin(0))
SERVER = '192.168.1.139'
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
TOPIC = b"kgrund"

def main(server=SERVER):
    """Measure and talk to MQTT broker"""
    c = MQTTClient(CLIENT_ID, server)
    c.connect
    print("Connected to {}".format(server))
    while true:
        d.measure()
        print("humidity: {}".format(d.humidity())
        c.publish(TOPIC, bytes(d.humidity()))
        time.sleep(20)
