from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from datetime import datetime

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    @app.template_filter('datetime')
    def format_datetime(timestamp):
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    
    from app.models.user import User
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    from app.routes import auth, copyright, blockchain
    app.register_blueprint(auth.bp)
    app.register_blueprint(copyright.bp)
    app.register_blueprint(blockchain.bp)
    
    return app