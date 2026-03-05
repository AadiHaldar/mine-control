from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class MinePacket(Base):
    __tablename__ = "mine_packets"

    id = Column(Integer, primary_key=True, index=True)
    node_id = Column(String)
    methane = Column(Float)
    temperature = Column(Float)
    vibration = Column(Float)
    ai_prediction = Column(String)
    emergency = Column(Boolean)
    risk_score = Column(Float) 
    source = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
