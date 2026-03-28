"""
example.py — End-to-end Smart Wallet SDK demo.

Run the backend first:
    uvicorn backend.app:app --reload

Then run this script:
    python example.py
"""

from sdk.client import SmartWalletClient

client = SmartWalletClient()

# 🔥 SINGLE CALL TO CONNECT WALLET
wallet_info = client.connect_wallet()
print("Connected:", wallet_info)

# 🔐 Sign a message
signature = client.sign_message("hello world")
print("Signature:", signature[:32], "…")

# 🪪 Create a persistent delegation (30-day grant)
delegation = client.create_delegation(
    permissions={
        "transfer": True,
        "sign": True
    }
)
print("Delegation created (expires_at):", delegation["payload"]["expires_at"])

# ♻️  Simulate app restart — load persisted delegation
client.load_delegation()
print("Delegation loaded:", client.delegation_token is not None)

# ⚡ Execute without re-authentication
try:
    result = client.execute_action(
        action="transfer",
        data={"to": "addr_123", "amount": 50}
    )
    print("Execution:", result)
except Exception as e:
    print("Execute error (backend not running?):", e)
