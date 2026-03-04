import time
import requests
from database import SessionLocal
from models import MinePacket

CLOUD_URL = "https://example.com/store"

def sync_loop():
    while True:
        db = SessionLocal()
        packets = db.query(MinePacket).all()

        for packet in packets:
            try:
                requests.post(CLOUD_URL, json={
                    "node_id": packet.node_id,
                    "methane": packet.methane
                }, timeout=3)
            except:
                pass

        time.sleep(30)