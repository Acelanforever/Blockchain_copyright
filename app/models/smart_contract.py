from datetime import datetime
from app import db
from app.models.blockchain import blockchain

class CopyrightContract(db.Model):
    # 定义CopyrightContract模型，用于存储版权转让合约信息
    id = db.Column(db.Integer, primary_key=True)  # 主键
    copyright_id = db.Column(db.Integer, db.ForeignKey('copyright.id'), nullable=False)  # 版权ID，外键引用Copyright模型的id
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 转让方ID，外键引用User模型的id
    transferee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # 受让方ID，外键引用User模型的id
    status = db.Column(db.String(20), default='pending')  # 合约状态，默认为pending，可能的状态有pending、confirmed、rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 创建时间，默认为当前时间
    
    # 定义关系
    copyright = db.relationship('Copyright', backref='transfer_contracts')  # 与Copyright模型的关系
    owner = db.relationship('User', foreign_keys=[owner_id], backref='transfer_out_contracts')  # 与User模型的关系，作为转让方
    transferee = db.relationship('User', foreign_keys=[transferee_id], backref='transfer_in_contracts')  # 与User模型的关系，作为受让方

    def confirm_transfer(self):
        """确认转让"""
        # 检查合约状态是否为pending
        if self.status != 'pending':
            return False, "合约状态无效"
            
        # 更新版权所有权，转让给受让方
        self.copyright.user_id = self.transferee_id
        # 更新合约状态为confirmed
        self.status = 'confirmed'

        # 准备转让信息，用于区块链记录
        transfer_data = {
            'type': 'copyright_transfer',  # 交易类型
            'copyright_id': self.copyright_id,  # 版权ID
            'contract_id': self.id,  # 合约ID
            'from_user': self.owner.username,  # 转让方用户名
            'to_user': self.transferee.username,  # 受让方用户名
            'timestamp': datetime.utcnow().timestamp()  # 时间戳
        }
        
        # 将转让信息添加到区块链的待处理交易列表
        blockchain.add_transaction(transfer_data)
        # 挖掘区块，确认转让
        blockchain.mine_pending_transactions(self.transferee.username)
        
        return True, "版权转让成功"
    def reject_transfer(self):
        """拒绝转让"""
        if self.status != 'pending':
            return False, "合约状态无效"
            
        self.status = 'rejected'
        return True, "已拒绝转让"

    # 添加新字段存储区块哈希
    block_hash = db.Column(db.String(64))  # 存储区块哈希的字段

class ContractTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 主键
    contract_id = db.Column(db.Integer, db.ForeignKey('copyright_contract.id'))  # 合约ID，外键引用CopyrightContract模型的id
    from_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 转让方ID，外键引用User模型的id
    to_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 受让方ID，外键引用User模型的id
    amount = db.Column(db.Float)  # 交易金额
    type = db.Column(db.String(20))  # 交易类型，可能的值有transfer（转让）和authorization（授权）
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  # 交易时间戳，默认为当前时间