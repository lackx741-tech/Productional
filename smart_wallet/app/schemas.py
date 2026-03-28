from typing import Literal

from pydantic import BaseModel


class WalletCreate(BaseModel):
    owner: str


class TransactionCreate(BaseModel):
    wallet_id: int
    amount: float
    type: Literal["credit", "debit"]
