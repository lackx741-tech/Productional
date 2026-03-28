# Productional — Smart Wallet System

A production-ready, modular Smart Wallet platform featuring:

- **Secure wallet management** with balance tracking
- **Transaction engine** — credit / debit with insufficient-funds enforcement
- **Event-driven REST API** (FastAPI)
- **Ops dashboard** (Streamlit)
- **SQLite persistence** (easily swappable for Postgres)
- **Single-button Wallet Connect SDK** (`connect_wallet()` entry point)
- **Persistent delegation** — sign once, act forever (within expiry)
- **ERC-4337 smart account** architecture (session keys, gasless UX)

---

## 🧠 Architecture

```
Productional/
│
├── smart_wallet/           # Core wallet API + dashboard
│   ├── app/
│   │   ├── main.py         # FastAPI application
│   │   ├── models.py       # SQLAlchemy ORM models
│   │   ├── db.py           # Database engine & session
│   │   ├── wallet_service.py
│   │   ├── transaction_service.py
│   │   └── schemas.py      # Pydantic request/response schemas
│   └── dashboard/
│       └── dashboard.py    # Streamlit ops dashboard
│
├── sdk/                    # Smart Wallet Connect SDK
│   ├── __init__.py
│   ├── client.py           # SmartWalletClient (single entry point)
│   ├── wallet.py           # In-memory wallet model
│   ├── signer.py           # RSA key generation & signing
│   ├── session.py          # Session lifecycle management
│   └── delegation.py       # Persistent delegation tokens
│
├── backend/
│   └── app.py              # Lightweight FastAPI backend for the SDK
│
├── contracts/
│   └── SmartAccount.sol    # ERC-4337 compliant smart account (Solidity)
│
├── example.py              # End-to-end SDK usage demo
└── requirements.txt
```

---

## ⚙️ Install

```bash
pip install -r requirements.txt
```

---

## 🚀 Run (end-to-end)

### Wallet API backend
```bash
# From the smart_wallet/ directory
uvicorn app.main:app --reload
```

### Ops dashboard
```bash
streamlit run smart_wallet/dashboard/dashboard.py
```

### SDK backend
```bash
uvicorn backend.app:app --port 8000 --reload
```

### SDK example
```bash
python example.py
```

---

## 📡 API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/wallet` | Create a new wallet |
| `GET` | `/wallet/{id}` | Get wallet details & balance |
| `POST` | `/transaction` | Credit or debit a wallet |
| `POST` | `/tx` | SDK: send a signed transaction |
| `POST` | `/execute` | SDK: execute a delegated action |

---

## 🔑 SDK — Single Button Usage

```python
from sdk.client import SmartWalletClient

client = SmartWalletClient()

# 🔥 One call to connect
wallet_info = client.connect_wallet()

# 🪪 Create a 30-day delegation (persist to disk)
client.create_delegation(permissions={"transfer": True, "sign": True})

# ♻️  App restart — reload without re-signing
client.load_delegation()

# ⚡ Execute without re-auth
client.execute_action("transfer", {"to": "addr_123", "amount": 50})
```

---

## 🧱 ERC-4337 Smart Account

`contracts/SmartAccount.sol` implements:

- Owner-controlled session keys
- `addSessionKey` / `revokeSessionKey`
- `validateSignature` supporting both owner EOA and delegated session keys
- Compatible with the ERC-4337 `UserOperation` flow

---

## 🔥 Key Features

| Feature | Status |
|---------|--------|
| Wallet creation | ✅ |
| Secure balance updates | ✅ |
| Credit/Debit enforcement | ✅ |
| Transaction history | ✅ |
| API-first architecture | ✅ |
| Live ops dashboard | ✅ |
| Single-button wallet connect | ✅ |
| RSA message signing | ✅ |
| Persistent delegation tokens | ✅ |
| Session expiry management | ✅ |
| Permission-based execution | ✅ |
| ERC-4337 smart account | ✅ |
