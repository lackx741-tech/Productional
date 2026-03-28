from sqlalchemy.orm import Session
from . import models


def create_wallet(db: Session, owner: str):
    wallet = models.Wallet(owner=owner, balance=0.0)
    db.add(wallet)
    db.commit()
    db.refresh(wallet)
    return wallet


def get_wallet(db: Session, wallet_id: int):
    return db.query(models.Wallet).filter(models.Wallet.id == wallet_id).first()


def update_balance(db: Session, wallet: models.Wallet, amount: float):
    wallet.balance += amount
    db.commit()
    db.refresh(wallet)
    return wallet
