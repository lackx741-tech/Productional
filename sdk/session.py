import time


class Session:
    def __init__(self, wallet_address: str, public_key: str):
        self.wallet_address = wallet_address
        self.public_key = public_key
        self.created_at = time.time()

    def is_active(self) -> bool:
        # 1 hour expiry
        return (time.time() - self.created_at) < 3600
