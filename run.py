from app import create_app, db

app = create_app()

# 在应用启动时初始化数据库
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
