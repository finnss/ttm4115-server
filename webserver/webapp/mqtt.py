import paho.mqtt.client as mqtt
from json import loads
from models import SensorReading

def verify_topic(topic): # almost certainly overkill
    topic = topic.split("/")
    if len(topic) != 4 or topic[0] != "plantlife" or topic[1] != "sensors" or topic[3] != "humidity":
        return -1
    try:
        res = int(topic[2])
        if res < 0:
            return -1
        return res
    except ValueError:
        return -1

def on_connect(client, userdata, rc):
    client.subscribe("plantlife/sensors/+/humidity", qos=2)

def on_message(client, userdata, msg):
    data = loads(msg.payload)
    data["sensor_id"] = verify_topic(msg.topic)
    if data["sensor_id"] == -1:
        # Something went wrong
        pass
    else:
        data["sensor_id"] #sensor serial number. should match on sensor and server
        data["humidity"] #float between and including 0. and 1.
        data["timestamp"] #epoch timestamp

client = mqtt.Client(client_id="plantlife-server", clean_session=False)
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)