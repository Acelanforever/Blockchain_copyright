from .block import Block
import time

class Blockchain:
    def __init__(self):
        self.chain = []
        self.difficulty = 4
        self.pending_transactions = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.calculate_hash()
        self.chain.append(genesis_block)

    def get_latest_block(self):
        return self.chain[-1]

    def add_transaction(self, transaction):
        self.pending_transactions.append(transaction)

    def mine_pending_transactions(self, miner_address):
        block = Block(len(self.chain), self.pending_transactions,
                     time.time(), self.get_latest_block().hash)
        
        block.mine_block(self.difficulty)
        self.chain.append(block)
        self.pending_transactions = []
        return block

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True 