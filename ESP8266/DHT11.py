"""Reads temperature and humidity from a DHT11 with a ESP8266 via MQTT."""
import machine
from dht import DHT11
import time
import ubinascii
from umqtt.simple import MQTTClient

# d = DHT11(machine.Pin(0))
SERVER = '192.168.1.8'
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
TOPIC = b'kgrund/fukt'


def main(server=SERVER):
    """Measure and talk to MQTT broker."""
    c = MQTTClient(CLIENT_ID, server)
    c.connect()
    # print('Connected to {}'.format(server))
    """while True:
        d.measure()
        c.publish(TOPIC, d.humidity())
        time.sleep(20)"""
    c.publish(TOPIC, b"hello")
    c.disconnect()

if __name__ == '__main__':
    main(SERVER)
