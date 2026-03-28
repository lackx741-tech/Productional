import time
import json


class Delegation:
    def __init__(self, signer):
        self.signer = signer

    def create_delegation(self, permissions: dict, expiry_seconds: int = 3600 * 24 * 30) -> dict:
        payload = {
            "permissions": permissions,
            "issued_at": int(time.time()),
            "expires_at": int(time.time()) + expiry_seconds
        }

        signature = self.signer.sign(json.dumps(payload, sort_keys=True).encode())

        return {
            "payload": payload,
            "signature": signature.hex()
        }

    def verify_delegation(self, delegation_token: dict) -> bool:
        payload = delegation_token["payload"]
        signature = bytes.fromhex(delegation_token["signature"])

        if time.time() > payload["expires_at"]:
            return False

        try:
            self.signer.verify(
                json.dumps(payload, sort_keys=True).encode(),
                signature
            )
            return True
        except Exception:
            return False
