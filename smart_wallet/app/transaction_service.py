from sqlalchemy.orm import Session
from . import models

CREDIT = "credit"
DEBIT = "debit"


def create_transaction(db: Session, wallet_id: int, amount: float, transaction_type: str):
    wallet = db.query(models.Wallet).filter(models.Wallet.id == wallet_id).first()

    if not wallet:
        raise ValueError("Wallet not found")

    if transaction_type == DEBIT and wallet.balance < amount:
        raise ValueError("Insufficient funds")

    final_amount = amount if transaction_type == CREDIT else -amount

    wallet.balance += final_amount

    tx = models.Transaction(
        wallet_id=wallet_id,
        amount=amount,
        type=transaction_type
    )

    db.add(tx)
    db.commit()
    db.refresh(tx)

    return tx
