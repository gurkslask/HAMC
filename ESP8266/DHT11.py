"""Reads temperature and humidity from a import DHT11 with a ESP8266."""
from machine import Pin
from dht import DHT11
from time import sleep
import socket

d = DHT11(Pin(0))
s = socket.socket()
addr = ('192.168.1.139', 5004)

while True:
    # d.measure()
    s.connect(addr)
    s.sendall(b'1')
    print('runt')
    sleep(5)
