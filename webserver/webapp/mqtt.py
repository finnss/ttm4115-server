import paho.mqtt.client as mqtt
from json import loads
import json
import requests
from datetime import datetime, timezone

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
    print("Sending message")


def on_message(client, userdata, msg):
    # Need to import these here because the file is loaded in __init__.py and you can't "load" models yet there.
    from .models import Sensor, SensorReading
    print('Received a MQTT message!')
    data = loads(msg.payload)
    print(data)

    data["sensor_id"] = verify_topic(msg.topic)
    if data["sensor_id"] == -1:
        print("Something went wrong.")
        pass

    else:
        moisture = int(data["humidity"] * 100)
        timestamp = datetime.fromtimestamp(data["timestamp"], timezone.utc)
        sensor = Sensor.objects.get_or_create(serial_number=data["sensor_id"])[0]
        sensor_reading = SensorReading.objects.create(moisture=moisture, timestamp=timestamp, sensor=sensor)

        if sensor.monitoring_plant:
            print("Found a plant to monitor")
            upper_moisture_bound = sensor.monitoring_plant.upper_moisture_bound or 101
            lower_moisture_bound = sensor.monitoring_plant.lower_moisture_bound or -1
            plant_string = "\nMonitored plant: " + str(sensor.monitoring_plant) + "\n"
        else:
            upper_moisture_bound = 101
            lower_moisture_bound = -1
            plant_string = ""

        return

        # Fyr av advarsel til bruker dersom vann-nivået er out of bounds
        if moisture > upper_moisture_bound or moisture < lower_moisture_bound:
            error_message = "much" if moisture > upper_moisture_bound else "little"
            print("Sending message")

            message_string = "---\nOut of bounds sensor reading detected!\nSensor id: " + str(data["sensor_id"])
            message_string += "\nTime: " + str(timestamp.strftime("%H:%M:%S %d-%m-%Y")) + "\n"
            message_string += plant_string
            message_string += "Expected humidity between " + str(lower_moisture_bound) + " and " + str(upper_moisture_bound) + "%, "
            message_string += "but read " + str(moisture) + ".\n"
            message_string += "There is too " + error_message + " water!\n"

            for user in sensor.interested_users.all():
                message_string += "@" + str(user) + " "

            message_string += "\n---"

            webhook_url = 'https://hooks.slack.com/services/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'
            slack_data = {'text': message_string}

            response = requests.post(
                webhook_url, data=json.dumps(slack_data),
                headers={'Content-Type': 'application/json'}
            )

            if response.status_code != 200:
                raise ValueError(
                    'Request to slack returned an error %s, the response is:\n%s'
                    % (response.status_code, response.text)
                )

        return sensor_reading


client = mqtt.Client(client_id="plantlife-server", clean_session=False)
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)
print("Successfully connected to MQTT broker.")
