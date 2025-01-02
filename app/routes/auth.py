from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User
from app import db

# 创建一个名为'auth'的蓝图，用于处理用户认证相关的路由
bp = Blueprint('auth', __name__, url_prefix='/auth')

# 注册路由，用于处理用户注册
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # 检查用户名是否已存在
        if User.query.filter_by(username=username).first():
            flash('用户名已存在')
            return redirect(url_for('auth.register'))
            
        # 检查邮箱是否已被注册
        if User.query.filter_by(email=email).first():
            flash('邮箱已被注册')
            return redirect(url_for('auth.register'))
            
        # 创建新用户
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        # 注册成功后，重定向到登录页面
        return redirect(url_for('auth.login'))
        
    # 如果是GET请求，返回注册页面
    return render_template('auth/register.html')

# 注册路由，用于处理用户登录
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        # 检查用户名和密码是否正确
        if user is None or not user.check_password(password):
            flash('用户名或密码错误')
            return redirect(url_for('auth.login'))
            
        # 登录成功后，重定向到首页
        login_user(user)
        return redirect(url_for('copyright.index'))
        
    # 如果是GET请求，返回登录页面
    return render_template('auth/login.html')

# 注册路由，用于处理用户登出
@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('copyright.index'))
