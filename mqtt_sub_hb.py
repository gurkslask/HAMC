import logging
import asyncio

from hbmqtt.client import MQTTClient, ClientException
from hbmqtt.mqtt.constants import QOS_1, QOS_2

@asyncio.coroutine
def uptime_coro():
    C = MQTTClient()
    yield from C.connect('mqtt://192.168.1.8')
    # Subscribe to '$SYS/broker/uptime' with QOS=1
    # Subscribe to '$SYS/broker/load/#' with QOS=2
    yield from C.subscribe([
        # ('$SYS/broker/uptime', QOS_1),
        # ('$SYS/broker/load/#', QOS_2),
        ('kgrund/fukt', QOS_1),
    ])
    try:
        for i in range(1, 100):
            message = yield from C.deliver_message()
            packet = message.publish_packet
            print("%d:  %s => %s" % (i, packet.variable_header.topic_name, str(packet.payload.data)))
        yield from C.unsubscribe(['$SYS/broker/uptime', '$SYS/broker/load/#'])
        yield from C.disconnect()
    except ClientException as ce:
        logger.error("Client exception: %s" % ce)

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(uptime_coro())
