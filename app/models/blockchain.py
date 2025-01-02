from .block import Block
import time
import hashlib

class Blockchain:
    def __init__(self):
        # 初始化区块链，包含区块链列表、难度、待处理交易列表，并创建创世区块
        self.chain = []
        self.difficulty = 4
        self.pending_transactions = []
        self.create_genesis_block()

    def create_genesis_block(self):
        # 创建创世区块
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.calculate_hash()
        self.chain.append(genesis_block)

    def get_latest_block(self):
        # 获取最新区块
        return self.chain[-1]

    def add_transaction(self, transaction):
        # 添加交易到待处理交易列表
        self.pending_transactions.append(transaction)

    def mine_pending_transactions(self, miner_address):
        # 挖掘待处理交易
        block = Block(len(self.chain), self.pending_transactions,
                     time.time(), self.get_latest_block().hash)
        
        block.mine_block(self.difficulty)
        self.chain.append(block)
        self.pending_transactions = []
        return block

    def is_chain_valid(self):
        # 检查区块链是否有效
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True 

# 创建全局区块链实例
blockchain = Blockchain()