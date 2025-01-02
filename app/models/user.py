from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(UserMixin, db.Model):
    # 定义用户模型的字段
    id = db.Column(db.Integer, primary_key=True)  # 用户ID，主键
    username = db.Column(db.String(64), unique=True, nullable=False)  # 用户名，唯一且不能为空
    email = db.Column(db.String(120), unique=True, nullable=False)  # 电子邮件，唯一且不能为空
    password_hash = db.Column(db.String(128))  # 密码哈希
    copyrights = db.relationship('Copyright', backref='author', lazy='dynamic')  # 定义与Copyright模型的关系

    def set_password(self, password):
        # 设置用户密码
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        # 检查用户密码是否正确
        return check_password_hash(self.password_hash, password) 