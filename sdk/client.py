import json
import requests
from .wallet import SmartWallet
from .signer import Signer
from .session import Session
from .delegation import Delegation


class SmartWalletClient:
    """Single-entry-point Smart Wallet Connect SDK."""

    def __init__(self, backend_url: str = "http://127.0.0.1:8000"):
        self.backend_url = backend_url
        self.wallet: SmartWallet | None = None
        self.signer: Signer | None = None
        self.session: Session | None = None
        self._delegation_mgr: Delegation | None = None
        self.delegation_token: dict | None = None

    # ─────────────────────────────────────────────────────────────────────────
    # SINGLE ENTRY POINT
    # ─────────────────────────────────────────────────────────────────────────

    def connect_wallet(self) -> dict:
        """Connect wallet — the single button SDK entry point.

        Initialises the wallet, signer and session in one call.
        """
        self.wallet = SmartWallet()
        self.signer = Signer()
        self._delegation_mgr = Delegation(self.signer)

        self.session = Session(
            wallet_address=self.wallet.address,
            public_key=self.signer.get_public_key()
        )

        return {
            "address": self.wallet.address,
            "public_key": self.signer.get_public_key(),
            "session_active": self.session.is_active()
        }

    # ─────────────────────────────────────────────────────────────────────────
    # SIGNING
    # ─────────────────────────────────────────────────────────────────────────

    def sign_message(self, message: str) -> str:
        if not self.signer:
            raise Exception("Wallet not connected")
        signature = self.signer.sign(message.encode())
        return signature.hex()

    # ─────────────────────────────────────────────────────────────────────────
    # TRANSACTIONS
    # ─────────────────────────────────────────────────────────────────────────

    def send_transaction(self, to: str, amount: float) -> dict:
        if not self.session or not self.session.is_active():
            raise Exception("Session expired or wallet not connected")

        payload = {
            "from": self.wallet.address,
            "to": to,
            "amount": amount,
            "signature": self.sign_message(f"{to}:{amount}")
        }

        res = requests.post(f"{self.backend_url}/tx", json=payload, timeout=30)
        res.raise_for_status()
        return res.json()

    # ─────────────────────────────────────────────────────────────────────────
    # PERSISTENT DELEGATION
    # ─────────────────────────────────────────────────────────────────────────

    def create_delegation(self, permissions: dict, persist_path: str = "delegation.json") -> dict:
        """Create and persist a delegation token."""
        if not self._delegation_mgr:
            raise Exception("Wallet not connected")

        self.delegation_token = self._delegation_mgr.create_delegation(permissions)

        with open(persist_path, "w") as f:
            json.dump(self.delegation_token, f)

        return self.delegation_token

    def load_delegation(self, persist_path: str = "delegation.json") -> dict | None:
        """Load a previously persisted delegation token."""
        try:
            with open(persist_path, "r") as f:
                self.delegation_token = json.load(f)
        except FileNotFoundError:
            self.delegation_token = None

        return self.delegation_token

    def execute_action(self, action: str, data: dict) -> dict:
        """Execute a delegated action without re-authentication."""
        if not self.delegation_token:
            raise Exception("No delegation found — call create_delegation() first")

        if not self._delegation_mgr or not self._delegation_mgr.verify_delegation(self.delegation_token):
            raise Exception("Invalid or expired delegation")

        payload = {
            "action": action,
            "data": data,
            "delegation": self.delegation_token
        }

        res = requests.post(f"{self.backend_url}/execute", json=payload, timeout=30)
        res.raise_for_status()
        return res.json()
