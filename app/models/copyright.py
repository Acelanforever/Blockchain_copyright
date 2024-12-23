from app import db
from datetime import datetime

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
            'timestamp': self.timestamp.isoformat(),
            'author': self.author.username,
            'block_hash': self.block_hash,
            'status': self.status
        } 