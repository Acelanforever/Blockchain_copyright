from flask import Blueprint, render_template, request, jsonify, current_app
from flask_login import login_required, current_user
from app.models.copyright import Copyright
from app.models.blockchain import Blockchain
from werkzeug.utils import secure_filename
import hashlib
import os
from app import db
from datetime import datetime

bp = Blueprint('copyright', __name__)
blockchain = Blockchain()

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def ensure_upload_folder():
    upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    return upload_folder

@bp.route('/')
def index():
    copyrights = Copyright.query.order_by(Copyright.timestamp.desc()).all()
    return render_template('copyright/index.html', copyrights=copyrights)

@bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': '没有文件'}), 400
            
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': '未选择文件'}), 400
            
        if file and allowed_file(file.filename):
            try:
                # 确保上传文件夹存在
                upload_folder = ensure_upload_folder()
                
                # 安全地获取文件名并保存文件
                filename = secure_filename(file.filename)
                file_path = os.path.join(upload_folder, filename)
                file.save(file_path)
                
                # 计算文件哈希
                with open(file_path, 'rb') as f:
                    content = f.read()
                    content_hash = hashlib.sha256(content).hexdigest()
                
                # 创建版权记录
                copyright = Copyright(
                    title=request.form['title'],
                    description=request.form['description'],
                    content_hash=content_hash,
                    user_id=current_user.id,
                    timestamp=datetime.utcnow()  # 显式设置时间戳
                )
                
                # 先保存到数据库，这样就会有 timestamp
                db.session.add(copyright)
                db.session.flush()  # 这会分配 ID 但不会提交事务
                
                # 添加到区块链
                transaction = copyright.to_dict()
                blockchain.add_transaction(transaction)
                block = blockchain.mine_pending_transactions(current_user.username)
                
                copyright.block_hash = block.hash
                copyright.status = 'confirmed'
                
                db.session.commit()  # 最后提交所有更改
                
                return jsonify({
                    'success': True, 
                    'copyright_id': copyright.id,
                    'message': '上传成功！'
                })
                
            except Exception as e:
                db.session.rollback()  # 发生错误时回滚
                current_app.logger.error(f"Upload error: {str(e)}")
                return jsonify({'error': f'上传失败：{str(e)}'}), 500
                
        return jsonify({'error': '不支持的文件类型'}), 400
            
    return render_template('copyright/upload.html')

@bp.route('/search')
def search():
    query = request.args.get('q', '')
    copyrights = Copyright.query.filter(
        Copyright.title.contains(query) | 
        Copyright.description.contains(query)
    ).all()
    return render_template('copyright/search.html', copyrights=copyrights)

@bp.route('/copyright/<int:id>')
def detail(id):
    copyright = Copyright.query.get_or_404(id)
    return render_template('copyright/detail.html', copyright=copyright)

@bp.route('/api/verify/<content_hash>')
def verify(content_hash):
    copyright = Copyright.query.filter_by(content_hash=content_hash).first()
    if copyright:
        return jsonify(copyright.to_dict())
    return jsonify({'error': '未找到相关版权信息'}), 404
