from shared.models.user_model import User

class UserRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    def get_by_id(self, user_id):
        user = self.db_session.query(User).filter_by(Id=user_id).first()
        return user

    def get_all(self):
        users = self.db_session.query(User).all()
        return users
