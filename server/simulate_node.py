
import requests
import random
import time

SERVER_URL = "https://mine-control.onrender.com/mine_packet"

while True:
    data = {
        "node_id": "NODE01",
        "methane": random.randint(100, 400),
        "temperature": random.randint(20, 60),
        "vibration": round(random.uniform(0.5, 2.0), 2),
        "ai_prediction": "Gas Risk",
        "emergency": random.choice([True, False])
    }

    response = requests.post(SERVER_URL, json=data)
    print("Sent:", data)
    print("Response:", response.json())
    time.sleep(5)
