import paho.mqtt.client as mqtt

def on_message(client, userdata, msg):
    print("MQTT:", msg.payload.decode())

client = mqtt.Client()
client.connect("localhost", 1883, 60)
client.subscribe("mine/data")
client.on_message = on_message
client.loop_start()