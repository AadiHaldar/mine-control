
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from models import Base, MinePacket
import requests
import datetime

# -----------------------------
# CREATE DATABASE TABLES
# -----------------------------
Base.metadata.create_all(bind=engine)

# -----------------------------
# INITIALIZE FASTAPI
# -----------------------------
app = FastAPI(title="IoT Mine Safety Control Server")

# Static files
app.mount("/static", StaticFiles(directory="server/static"), name="static")

# Templates
templates = Jinja2Templates(directory="server/templates")

# -----------------------------
# DATA MODEL (Incoming Packet)
# -----------------------------
class Packet(BaseModel):
    node_id: str
    methane: float
    temperature: float
    vibration: float
    ai_prediction: str
    emergency: bool


# -----------------------------
# CLOUD CONFIG
# -----------------------------
CLOUD_URL = "https://example.com/store"


# -----------------------------
# RISK AI ENGINE
# -----------------------------
def calculate_risk(packet: Packet):
    risk_score = (
        packet.methane * 0.5 +
        packet.temperature * 0.3 +
        packet.vibration * 20
    )

    explanation = []

    if packet.methane > 300:
        explanation.append("High Methane")

    if packet.temperature > 50:
        explanation.append("High Temperature")

    if packet.vibration > 1.5:
        explanation.append("Abnormal Vibration")

    if not explanation:
        explanation.append("Normal Conditions")

    return risk_score, ", ".join(explanation)


# -----------------------------
# RECEIVE PACKET ENDPOINT
# -----------------------------
@app.post("/mine_packet")
def receive_packet(packet: Packet):

    db: Session = SessionLocal()

    try:
        risk_score, explanation = calculate_risk(packet)

        auto_emergency = risk_score > 250

        db_packet = MinePacket(
            node_id=packet.node_id,
            methane=packet.methane,
            temperature=packet.temperature,
            vibration=packet.vibration,
            ai_prediction=explanation,
            emergency=auto_emergency,
            risk_score=risk_score,
            timestamp=datetime.datetime.utcnow()
        )

        db.add(db_packet)
        db.commit()

        # Try sending to cloud
        try:
            requests.post(
                CLOUD_URL,
                json={**packet.dict(), "risk_score": risk_score},
                timeout=3
            )
        except Exception:
            print("Cloud unreachable. Stored locally.")

        return {
            "status": "Packet stored successfully",
            "risk_score": risk_score,
            "explanation": explanation
        }

    finally:
        db.close()


# -----------------------------
# DASHBOARD UI
# -----------------------------
@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):

    db: Session = SessionLocal()

    try:
        packets = (
            db.query(MinePacket)
            .order_by(MinePacket.id.desc())
            .limit(20)
            .all()
        )

        total = db.query(MinePacket).count()
        emergencies = db.query(MinePacket).filter(MinePacket.emergency == True).count()

        avg_risk_records = db.query(MinePacket.risk_score).all()

        avg_risk_value = (
            round(sum([r[0] for r in avg_risk_records]) / len(avg_risk_records), 2)
            if avg_risk_records else 0
        )

        return templates.TemplateResponse(
            "dashboard.html",
            {
                "request": request,
                "packets": packets,
                "total": total,
                "emergencies": emergencies,
                "avg_risk": avg_risk_value
            }
        )

    finally:
        db.close()


# -----------------------------
# API ENDPOINTS
# -----------------------------
@app.get("/packets")
def get_packets():

    db: Session = SessionLocal()

    try:
        return db.query(MinePacket).all()
    finally:
        db.close()


@app.get("/stats")
def stats():

    db: Session = SessionLocal()

    try:
        total = db.query(MinePacket).count()
        emergencies = db.query(MinePacket).filter(MinePacket.emergency == True).count()

        return {
            "total_packets": total,
            "emergency_count": emergencies
        }

    finally:
        db.close()


@app.get("/analytics")
def analytics():

    db: Session = SessionLocal()

    try:
        packets = db.query(MinePacket).order_by(MinePacket.id.asc()).all()

        methane = [p.methane for p in packets]
        temperature = [p.temperature for p in packets]
        vibration = [p.vibration for p in packets]
        risk = [p.risk_score for p in packets]
        timestamps = [str(p.timestamp) for p in packets]

        return {
            "timestamps": timestamps,
            "methane": methane,
            "temperature": temperature,
            "vibration": vibration,
            "risk": risk
        }

    finally:
        db.close()
```
