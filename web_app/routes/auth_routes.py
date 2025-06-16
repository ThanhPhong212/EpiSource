from flask_restx import Namespace, Resource, fields
from flask import request
from shared.repository import UserRepository
from web_app.services.auth_service import AuthService
from shared.db import db

api = Namespace('auth', path='/auth', description='Authentication APIs')

user_login_model = api.model('UserLogin', {
    'user_id': fields.Integer(required=True, description='User ID'),
})

@api.route('/login')
class Login(Resource):
    @api.expect(user_login_model)
    def post(self):
        user_repo = UserRepository(db.session)
        auth_service = AuthService(user_repo)
        user_id = request.json.get('user_id')
        return auth_service.login(user_id)

@api.route('/logout')
class Logout(Resource):
    def get(self):
        user_repo = UserRepository(db.session)
        auth_service = AuthService(user_repo)
        return auth_service.logout()
