from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime
from datetime import datetime, timezone
from .db import Base


def _utcnow():
    return datetime.now(timezone.utc)


class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True, index=True)
    owner = Column(String, unique=True, index=True)
    balance = Column(Float, default=0.0)
    created_at = Column(DateTime, default=_utcnow)


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    wallet_id = Column(Integer, ForeignKey("wallets.id"), index=True)
    amount = Column(Float)
    type = Column(String)  # credit / debit
    timestamp = Column(DateTime, default=_utcnow)
