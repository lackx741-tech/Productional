from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .db import Base, engine, get_db
from . import models, schemas, wallet_service, transaction_service

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Wallet System")


@app.post("/wallet")
def create_wallet(payload: schemas.WalletCreate, db: Session = Depends(get_db)):
    return wallet_service.create_wallet(db, payload.owner)


@app.get("/wallet/{wallet_id}")
def get_wallet(wallet_id: int, db: Session = Depends(get_db)):
    wallet = wallet_service.get_wallet(db, wallet_id)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return wallet


@app.post("/transaction")
def create_transaction(payload: schemas.TransactionCreate, db: Session = Depends(get_db)):
    try:
        return transaction_service.create_transaction(
            db,
            payload.wallet_id,
            payload.amount,
            payload.type
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
