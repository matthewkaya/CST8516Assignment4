from flask import Flask, jsonify, request
import paho.mqtt.client as mqtt
import threading
import time
import random

app = Flask(__name__)

# MQTT broker configuration
broker_address = "broker.hivemq.com"
topic = "temperature"
client = mqtt.Client()
retry_count = 3  # Number of retry attempts for connection
retry_delay = 2  # Delay in seconds between retry attempts
publishing = False  # Global flag to control publishing loop

# Task 1: Retry Mechanism
def connect_with_retry():
    """
    This function attempts to connect to the MQTT broker with a retry mechanism.
    If the connection fails, it retries 'retry_count' times with a delay of 'retry_delay' seconds.
    """
    for attempt in range(retry_count):
        try:
            client.connect(broker_address)
            print("Connected to MQTT Broker")
            return
        except Exception as e:
            print(f"Connection failed: {e}, retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
    print("Failed to connect to MQTT Broker after retries")

# Task 2: Random Temperature Publishing
def publish_temperature():
    """
    This function generates random temperature values between -10 and 40 degrees Celsius
    and publishes them to the MQTT broker at regular intervals.
    """
    global publishing
    while publishing:
        try:
            # Generate a random temperature value
            temp = round(random.uniform(-10, 40), 2)
            client.publish(topic, temp)
            print(f"Published temperature: {temp} to topic: {topic}")
        except Exception as e:
            print(f"Failed to publish: {e}")
        time.sleep(5)  # Delay between publishing

# Flask API Endpoints
@app.route('/start', methods=['POST'])
def start_publishing():
    """
    Start the temperature publishing process. This endpoint starts the background thread
    that generates and publishes random temperature values.
    """
    global publishing
    if not publishing:
        publishing = True
        threading.Thread(target=publish_temperature, daemon=True).start()
        return jsonify({"message": "Started publishing temperature data"})
    else:
        return jsonify({"message": "Already publishing"}), 400

def stop_publishing():
    """
    Stop the temperature publishing process. This endpoint stops the background thread.
    """
    global publishing
    if publishing:
        publishing = False
        return jsonify({"message": "Stopped publishing temperature data"})
    else:
        return jsonify({"message": "Not currently publishing"}), 400

@app.route('/publish', methods=['POST'])
def publish_custom():
    """
    Publish a custom temperature value provided by the user. This endpoint
    takes a JSON payload with a 'temperature' field and publishes it.
    """
    data = request.json
    if 'temperature' in data:
        try:
            client.publish(topic, data['temperature'])
            return jsonify({"message": f"Published custom temperature: {data['temperature']}"})
        except Exception as e:
            return jsonify({"error": f"Failed to publish: {e}"}), 500
    else:
        return jsonify({"error": "Temperature value not provided"}), 400

if __name__ == "__main__":
    # Connect to MQTT broker with retry mechanism
    connect_with_retry()
    # Start Flask application
    app.run(host='0.0.0.0', port=5000)