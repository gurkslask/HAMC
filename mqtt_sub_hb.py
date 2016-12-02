"""Coroutine that subscribes to topics from raspberry import pi broker."""
import asyncio

from hbmqtt.client import MQTTClient, ClientException
from hbmqtt.mqtt.constants import QOS_1


@asyncio.coroutine
def uptime_coro(data_func):
    """Coroutine that talks to raspberry broker, yields if it gets data."""
    c = MQTTClient()
    topic_1 = 'kgrund/fukt'
    topic_2 = 'kgrund/temp'
    yield from c.connect('mqtt://192.168.1.8')
    # Subscribe to '$SYS/broker/uptime' with QOS=1
    # Subscribe to '$SYS/broker/load/#' with QOS=2
    yield from c.subscribe([
        # ('$SYS/broker/uptime', QOS_1),
        # ('$SYS/broker/load/#', QOS_2),
        (topic_1, QOS_1),
        (topic_2, QOS_1),
    ])
    try:
        while True:
            future = asyncio.Future()
            future.add_done_callback(data_func)
            message = yield from c.deliver_message()
            packet = message.publish_packet
            print('%s => %s' % (
                packet.variable_header.topic_name, str(packet.payload.data)
                ))
            future.set_result(packet.payload.data)
        yield from c.unsubscribe([topic_1, topic_2])
        yield from c.disconnect()
    except ClientException as ce:
        print('Client exception: %s' % ce)

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(uptime_coro())
