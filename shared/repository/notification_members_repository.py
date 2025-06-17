from shared.models.notification_members_model import NotificationMembers

class NotificationMembersRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    def get_by_user_id_post_id(self, user_id, post_id):
        member = self.db_session.query(NotificationMembers).filter_by(UserId=user_id, PostId=post_id).first()
        return member

    def get_all(self):
        triggers = self.db_session.query(NotificationMembers).all()
        return triggers
    
    def delete_by_user_id_post_id(self, user_id, post_id):
        self.db_session.query(NotificationMembers) \
            .filter(NotificationMembers.UserId == user_id, NotificationMembers.PostId == post_id) \
            .delete(synchronize_session=False)
        self.db_session.commit()
