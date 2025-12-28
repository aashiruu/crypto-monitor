from web3 import Web3
from config import RPC_URL
import time


class BlockchainClient:
    def __init__(self):
        self.rpc_url = RPC_URL
        self.w3 = None
        self.connect()

    def connect(self):
        self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))

        if not self.w3.is_connected():
            print("WARNING: Ethereum RPC not reachable, retrying...")
            self.w3 = None

    def ensure_connection(self):
        if self.w3 is None:
            self.connect()
            time.sleep(5)

    def latest_block(self) -> int:
        self.ensure_connection()
        return self.w3.eth.block_number

    def get_block(self, block_number: int):
        self.ensure_connection()
        return self.w3.eth.get_block(block_number, full_transactions=True)

