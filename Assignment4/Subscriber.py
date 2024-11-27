import paho.mqtt.client as mqtt

broker_address = "broker.hivemq.com"
topic = "temperature"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(topic)

def on_message(client, userdata, msg):
    print("Received temperature:", msg.payload.decode())

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_address, 1883)
client.loop_start()

# Keep the main thread running to continue the execution of your application
while True:
    pass
