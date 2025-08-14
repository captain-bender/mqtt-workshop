# mqtt_workshop/sensor_simulator/main.py
import paho.mqtt.client as mqtt
import time
import json
import random

# mqtt_workshop/sensor_simulator/main.py
import paho.mqtt.client as mqtt
import time
import json
import random

BROKER_HOSTNAME = "mqtt_broker"
BROKER_PORT = 1883

def connect_mqtt():
    # Using the modern V2 client constructor
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "smart_building_simulator")
    client.connect(BROKER_HOSTNAME, BROKER_PORT)
    return client

def publish_data(client):
    print("Simulator is running. Publishing data...")
    while True:
        # Data for Room 101
        temp = {'value': round(random.uniform(20.0, 22.5), 1), 'unit': 'C'}
        humidity = {'value': round(random.uniform(45, 55), 1), 'unit': '%'}
        client.publish("smartbuilding/floor1/room101/temperature", json.dumps(temp))
        client.publish("smartbuilding/floor1/room101/humidity", json.dumps(humidity))
        print(f"Published Room 101 data: Temp={temp['value']}C, Humidity={humidity['value']}%")

        # Data for Room 102
        occupancy = {'occupied': random.choice([True, False])}
        light_level = {'value': random.randint(150, 500), 'unit': 'lux'}
        client.publish("smartbuilding/floor1/room102/occupancy", json.dumps(occupancy))
        client.publish("smartbuilding/floor1/room102/light_level", json.dumps(light_level))
        print(f"Published Room 102 data: Occupied={occupancy['occupied']}, Light={light_level['value']} lux")

        print("---")
        time.sleep(5)

if __name__ == '__main__':
    mqtt_client = connect_mqtt()
    mqtt_client.loop_start()
    publish_data(mqtt_client)