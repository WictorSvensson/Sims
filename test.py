import os
import time
import sys
import paho.mqtt.client as mqtt
import json

THINGSBOARD_HOST = '127.0.0.1'
ACCESS_TOKEN = '3Ahj265FzP0o6Jn50Ohw'

# Data capture and upload interval in seconds. Less interval will eventually hang the DHT22.
INTERVAL=2

sensor_data = {'Temperature': 0, 'pH': 0}

next_reading = time.time()

client = mqtt.Client()

# Set access token
client.username_pw_set(ACCESS_TOKEN)

# Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
client.connect(THINGSBOARD_HOST, 1883, 60)

client.loop_start()

try:
    while True:
        pH = 5
        temperature = 6
        pH = round(pH, 2)
        temperature = round(temperature, 2)
        print(u"Temperature: {:g}\u00b0C, pH: {:g}%".format(temperature, pH))
        sensor_data['temperature'] = temperature
        sensor_data['pH'] = pH

        # Sending humidity and temperature data to ThingsBoard
        client.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)

        next_reading += INTERVAL
        sleep_time = next_reading-time.time()
        if sleep_time > 0:
            time.sleep(sleep_time)
except KeyboardInterrupt:
    pass

client.loop_stop()
client.disconnect()