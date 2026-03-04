
# IoT Mine Safety Server

## Setup Instructions

1. Install dependencies:
   pip install -r requirements.txt

2. Run the server:
   uvicorn main:app --host 0.0.0.0 --port 8000

3. Simulate a node (optional):
   python simulate_node.py

Server API:
POST /mine_packet
GET  /packets

Local DB: SQLite (local_mine.db)
