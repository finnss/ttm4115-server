import paho.mqtt.client as mqtt
from json import loads


def verify_topic(topic):  # almost certainly overkill
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
    # Need to import these here because the file is loaded in __init__.py and you can't "load" models yet there.
    from .models import Sensor, SensorReading
    print('Received a MQTT message!')
    print(msg)
    data = loads(msg.payload)
    data["sensor_id"] = verify_topic(msg.topic)
    if data["sensor_id"] == -1:
        # Something went wrong
        print("Something went wrong.")
        pass
    else:
        sensor = Sensor.objects.get_or_create(serial_number=data["sensor_id"])[0]
        sensor_reading = SensorReading.objects.create(moisture=data["moisture"], timestamp=data["timestamp"], sensor=sensor)
        print('Stored!')
        print(sensor_reading)
        return sensor_reading


client = mqtt.Client(client_id="plantlife-server", clean_session=False)
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)
print("Successfully connected to MQTT broker.")
