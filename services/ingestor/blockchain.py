import time
from web3 import Web3
from config import RPC_URL

class BlockchainClient:
    def __init__(self):
        self.rpc_url = RPC_URL
        self.w3 = None
        self.connect()

    def connect(self):
        try:
            if not self.rpc_url:
                print("WARNING: RPC_URL not set")
                self.w3 = None
                return

            w3 = Web3(Web3.HTTPProvider(self.rpc_url))
            if w3.is_connected():
                self.w3 = w3
            else:
                print("WARNING: Ethereum RPC not reachable, retrying...")
                self.w3 = None
        except Exception as e:
            print(f"ERROR connecting to RPC: {e}")
            self.w3 = None

    def ensure_connection(self):
        if self.w3 is None:
            self.connect()
            time.sleep(3)

    def latest_block(self) -> int:
        while True:
            self.ensure_connection()
            if self.w3 is not None:
                return self.w3.eth.block_number
            time.sleep(3)

    def get_block(self, block_number: int):
        while True:
            self.ensure_connection()
            if self.w3 is not None:
                return self.w3.eth.get_block(block_number, full_transactions=True)
            time.sleep(3)
