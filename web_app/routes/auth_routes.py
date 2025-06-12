from flask import Blueprint, render_template, request
from shared.repository import UserRepository
from web_app.services.auth_service import AuthService
from shared.db import db

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    user_repo = UserRepository(db.session)
    auth_service = AuthService(user_repo)

    users = user_repo.get_all()

    if request.method == 'POST':
        user_id = int(request.form.get('user_id'))
        return auth_service.login(user_id)

    return render_template('login.html', users=users)


@auth_bp.route('/logout')
def logout():
    user_repo = UserRepository(db.session)
    auth_service = AuthService(user_repo)
    return auth_service.logout()
