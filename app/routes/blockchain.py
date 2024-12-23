from flask import Blueprint, render_template, jsonify
from app.models.blockchain import blockchain, Block
from app.models.copyright import Copyright
from app import db

bp = Blueprint('blockchain', __name__, url_prefix='/blockchain')

def sync_blockchain_with_db():
    """同步数据库中的版权记录到区块链"""
    # 如果区块链只有创世区块，则需要同步
    if len(blockchain.chain) <= 1:
        # 获取所有已确认的版权记录
        copyrights = Copyright.query.filter_by(status='confirmed').order_by(Copyright.timestamp).all()
        
        for copyright in copyrights:
            # 将版权信息添加到区块链
            transaction = copyright.to_dict()
            blockchain.add_transaction(transaction)
            
            # 使用原始时间戳创建区块
            timestamp = copyright.timestamp.timestamp()  # 转换为 UNIX 时间戳
            block = Block(
                index=len(blockchain.chain),
                transactions=blockchain.pending_transactions,
                timestamp=timestamp,  # 使用原始时间戳
                previous_hash=blockchain.get_latest_block().hash
            )
            
            # 挖矿
            block.mine_block(blockchain.difficulty)
            blockchain.chain.append(block)
            blockchain.pending_transactions = []
            
            # 更新数据库中的区块哈希
            copyright.block_hash = block.hash
            db.session.commit()

@bp.route('/explorer')
def explorer():
    """区块链浏览器主页"""
    # 确保区块链与数据库同步
    sync_blockchain_with_db()
    
    blocks = [{
        'index': block.index,
        'hash': block.hash,
        'previous_hash': block.previous_hash,
        'timestamp': block.timestamp,
        'transactions': len(block.transactions)
    } for block in blockchain.chain]
    
    return render_template('blockchain/explorer.html', blocks=blocks)

@bp.route('/api/blocks')
def get_blocks():
    """获取所有区块的API"""
    blocks = [{
        'index': block.index,
        'hash': block.hash,
        'previous_hash': block.previous_hash,
        'timestamp': block.timestamp,
        'transactions': block.transactions
    } for block in blockchain.chain]
    return jsonify(blocks)

@bp.route('/api/block/<int:index>')
def get_block(index):
    """获取特定区块的API"""
    if index < len(blockchain.chain):
        block = blockchain.chain[index]
        return jsonify({
            'index': block.index,
            'hash': block.hash,
            'previous_hash': block.previous_hash,
            'timestamp': block.timestamp,
            'transactions': block.transactions
        })
    return jsonify({'error': '区块不存在'}), 404 