from flask import session, redirect, url_for

class AuthService:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def login(self, user_id):
        session['user_id'] = user_id
        return redirect(url_for('post.index'))

    def logout(self):
        session.pop('user_id', None)
        return redirect(url_for('auth.login'))
