from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.smart_contract import CopyrightContract
from app.models.copyright import Copyright
from app import db
from app.models.blockchain import blockchain  # 导入区块链实例

bp = Blueprint('contract', __name__, url_prefix='/contract')

@bp.route('/transfer/<int:copyright_id>', methods=['GET', 'POST'])
@login_required
def initiate_transfer(copyright_id):
    """发起版权转让"""
    copyright = Copyright.query.get_or_404(copyright_id)
    
    # 验证是否是版权所有者
    if copyright.user_id != current_user.id:
        flash('你不是该版权的所有者')
        return redirect(url_for('copyright.detail', id=copyright_id))
        
    if request.method == 'POST':
        transferee_username = request.form['transferee']
        from app.models.user import User
        transferee = User.query.filter_by(username=transferee_username).first()
        
        if not transferee:
            flash('接收方用户不存在')
            return redirect(url_for('contract.initiate_transfer', copyright_id=copyright_id))
            
        contract = CopyrightContract(
            copyright_id=copyright_id,
            owner_id=current_user.id,
            transferee_id=transferee.id
        )
        
        db.session.add(contract)
        db.session.commit()
        
        flash('转让请求已发送')
        return redirect(url_for('copyright.detail', id=copyright_id))
        
    return render_template('contract/transfer.html', copyright=copyright)

@bp.route('/verify/<int:copyright_id>')
def verify_owner(copyright_id):
    """验证版权所有者"""
    copyright = Copyright.query.get_or_404(copyright_id)
    
    # 只查询必要的字段
    transfer_history = db.session.query(
        CopyrightContract.id,
        CopyrightContract.created_at,
        CopyrightContract.owner_id,
        CopyrightContract.transferee_id
    ).filter_by(
        copyright_id=copyright_id,
        status='confirmed'
    ).order_by(CopyrightContract.created_at.desc()).all()
    
    # 从区块链获取转让记录
    blockchain_records = []
    for block in blockchain.chain:
        for transaction in block.transactions:
            if (isinstance(transaction, dict) and 
                transaction.get('type') == 'copyright_transfer' and 
                transaction.get('copyright_id') == copyright_id):
                transaction['block_hash'] = block.hash
                blockchain_records.append(transaction)
    
    return render_template('contract/verify.html', 
                         copyright=copyright,
                         transfer_history=transfer_history,
                         blockchain_records=blockchain_records)

@bp.route('/confirm/<int:contract_id>', methods=['POST'])
@login_required
def confirm_transfer(contract_id):
    """确认转让"""
    contract = CopyrightContract.query.get_or_404(contract_id)
    
    # 验证是否是接收方
    if contract.transferee_id != current_user.id:
        return jsonify({'error': '你不是该转让的接收方'}), 403
        
    success, message = contract.confirm_transfer()
    if success:
        db.session.commit()
        flash('版权转让已确认')
    else:
        flash(message)
        
    return redirect(url_for('copyright.detail', id=contract.copyright_id)) 