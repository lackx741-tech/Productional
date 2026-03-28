from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import time

app = FastAPI(title="Smart Wallet Backend")


class TxRequest(BaseModel):
    from_addr: str = Field(alias="from")
    to: str
    amount: float
    signature: str

    model_config = {"populate_by_name": True}


class DelegationPayload(BaseModel):
    payload: dict
    signature: str


class ExecuteRequest(BaseModel):
    action: str
    data: dict
    delegation: DelegationPayload


@app.post("/tx")
def process_tx(tx: TxRequest):
    return {
        "status": "success",
        "from": tx.from_addr,
        "to": tx.to,
        "amount": tx.amount
    }


@app.post("/execute")
def execute(req: ExecuteRequest):
    payload = req.delegation.payload

    # Expiry check
    if time.time() > payload.get("expires_at", 0):
        raise HTTPException(status_code=403, detail="Delegation expired")

    permissions = payload.get("permissions", {})

    if not permissions.get(req.action, False):
        raise HTTPException(status_code=403, detail="Action not permitted")

    return {
        "status": "executed",
        "action": req.action,
        "data": req.data
    }
