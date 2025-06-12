from flask import session, flash, redirect, url_for, render_template, request

class AuthService:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def login(self, user_id):
        if request.method == 'POST':
            try:
                user = self.user_repository.get_by_id(user_id)
                if user:
                    session['user_id'] = user_id
                    flash('Đăng nhập thành công!', 'success')
                    return redirect(url_for('main.index'))
                else:
                    flash('Người dùng không tồn tại!', 'danger')
            except Exception as e:
                print("An error occurred:", e)
                flash('Lỗi đăng nhập!', 'danger')
        return render_template('login.html', users=users)

    def logout(self):
        session.pop('user_id', None)
        flash('Đã đăng xuất!', 'success')
        return redirect(url_for('main.login'))