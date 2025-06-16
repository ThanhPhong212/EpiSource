from flask_jwt_extended import create_access_token
class AuthService:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def login(self, user_id):
        user = self.user_repository.get_by_id(user_id)

        if not user:
            return {"message": "User not found"}, 404
        access_token = create_access_token(identity=user_id)
        return {
            "message": "Login successful",
            "access_token": access_token,
            "user": {
                "id": user.Id,
                "name": user.Name,
                "email": user.Email
            }
        }, 200

    def logout(self):
        return {"message": "Logged out"}, 200
