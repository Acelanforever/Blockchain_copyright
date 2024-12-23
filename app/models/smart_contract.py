from datetime import datetime
from app import db
from app.models.blockchain import blockchain

class CopyrightContract(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    copyright_id = db.Column(db.Integer, db.ForeignKey('copyright.id'), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    transferee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关系
    copyright = db.relationship('Copyright', backref='transfer_contracts')
    owner = db.relationship('User', foreign_keys=[owner_id], backref='transfer_out_contracts')
    transferee = db.relationship('User', foreign_keys=[transferee_id], backref='transfer_in_contracts')

    def confirm_transfer(self):
        """确认转让"""
        if self.status != 'pending':
            return False, "合约状态无效"
            
        # 更新版权所有权
        self.copyright.user_id = self.transferee_id
        self.status = 'confirmed'

        # 将转让信息记录到区块链
        transfer_data = {
            'type': 'copyright_transfer',
            'copyright_id': self.copyright_id,
            'contract_id': self.id,
            'from_user': self.owner.username,
            'to_user': self.transferee.username,
            'timestamp': datetime.utcnow().timestamp()
        }
        
        # 添加到区块链
        blockchain.add_transaction(transfer_data)
        blockchain.mine_pending_transactions(self.transferee.username)
        
        return True, "版权转让成功"

    def reject_transfer(self):
        """拒绝转让"""
        if self.status != 'pending':
            return False, "合约状态无效"
            
        self.status = 'rejected'
        return True, "已拒绝转让"

    # 添加新字段存储区块哈希
    block_hash = db.Column(db.String(64))

class ContractTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contract_id = db.Column(db.Integer, db.ForeignKey('copyright_contract.id'))
    from_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    to_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    amount = db.Column(db.Float)
    type = db.Column(db.String(20))  # transfer, authorization
    timestamp = db.Column(db.DateTime, default=datetime.utcnow) 