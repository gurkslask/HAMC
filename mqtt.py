import paho.mqtt.publish as publish


def publish_mqtt(topic, data):
    """Publish to MQTT server."""
    server = '192.168.1.19'
    publish.single('VS1/' + topic, data, hostname=server)

if __name__ == '__main__':
    publish_mqtt('test', 42)
