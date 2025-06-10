from app import create_app, db
from sqlalchemy import text
from app.models import User

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        try:
            db.session.execute(text('SELECT 1'))
            print('✅ Đã kết nối database thành công!')
        except Exception as e:
            print('❌ Kết nối database thất bại:', e)
        db.create_all()
    app.run(debug=True)
