"""Reads temperature and humidity from a DHT11 with a ESP8266 via MQTT."""
import machine
from dht import DHT11
import time
import ubinascii
from umqtt.simple import MQTTClient


def main():
    """Measure and talk to MQTT broker."""
    d = DHT11(machine.Pin(0))
    SERVER = '192.168.1.19'
    CLIENT_ID = ubinascii.hexlify(machine.unique_id())
    TOPIC_HUMIDITY = b'A001/KG_GM41'
    TOPIC_TEMPERATURE = b'A001/KG_GT41'
    c = MQTTClient(CLIENT_ID, SERVER)
    c.connect()
    print('Connected to {}'.format(SERVER))
    while True:
        """Measure and then publish values to the broker every 20 seconds."""
        try:
            d.measure()
            humidity = bytes(str(d.humidity()), 'ascii')
            temperature = bytes(str(d.temperature()), 'ascii')
            try:
                c.publish(TOPIC_HUMIDITY, humidity)
                c.publish(TOPIC_TEMPERATURE, temperature)
            except Exception:
                print('Cant publish to MQTT server, will try again')
        except Exception:
            print('Cant find DHT, will try again')
        time.sleep(20)

if __name__ == '__main__':
    main()
