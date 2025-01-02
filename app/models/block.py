import hashlib
import time
import json

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash):
        # 初始化区块的索引
        self.index = index
        # 初始化区块中的交易列表
        self.transactions = transactions
        # 初始化区块的时间戳
        self.timestamp = timestamp
        # 初始化区块的前一个区块的哈希值
        self.previous_hash = previous_hash
        # 初始化区块的nonce值，用于区块的挖矿
        self.nonce = 0
        # 计算并初始化区块的哈希值
        self.hash = self.calculate_hash()
    def calculate_hash(self):
        block_string = json.dumps({
            # 区块索引
            "index": self.index,
            # 区块中的交易列表
            "transactions": self.transactions,
            # 区块的时间戳
            "timestamp": self.timestamp,
            # 前一个区块的哈希值
            "previous_hash": self.previous_hash,
            # 区块的nonce值，用于区块的挖矿
            "nonce": self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty):
        target = "0" * difficulty
        # 当区块的哈希值的前difficulty位不等于目标值时，继续挖矿
        while self.hash[:difficulty] != target:
            # 增加nonce值
            self.nonce += 1
            # 重新计算区块的哈希值
            self.hash = self.calculate_hash()
        # 当挖矿完成后，返回区块的哈希值
        return self.hash 