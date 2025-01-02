from app import db
from datetime import datetime
# 定义Copyright模型，用于存储版权信息
# Copyright模型包含id、标题、描述、内容哈希、时间戳、用户ID、区块哈希和状态等字段

class Copyright(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    content_hash = db.Column(db.String(64), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    block_hash = db.Column(db.String(64))
    status = db.Column(db.String(20), default='pending')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'content_hash': self.content_hash,
            'timestamp': self.timestamp.timestamp(),
            'author': self.author.username,
            'block_hash': self.block_hash,
            'status': self.status
        } 