from shared.models import NotificationMembers, NotificationTrigger
from shared.db import db

class PostService:
    def __init__(self, post_repository, notification_members_repository, notification_trigger_repository):
        self.post_repository = post_repository
        self.notification_members_repository = notification_members_repository
        self.notification_trigger_repository = notification_trigger_repository

    def get_all(self):
        return self.post_repository.get_all()

    def get_by_id(self, post_id):
        return self.post_repository.get_by_id(post_id)

    def update_price(self, post, price):
        post.Price = price
        db.session.commit()

    def increase_view_count(self, post):
        post.ViewCount = (post.ViewCount or 0) + 1
        db.session.commit()

    def is_followed(self, user_id, post_id):
        return self.notification_members_repository.get_by_user_id_post_id(user_id, post_id) is not None

    def follow(self, user_id, post_id):
        if not self.is_followed(user_id, post_id):
            new_member = NotificationMembers(UserId=user_id, PostId=post_id)
            db.session.add(new_member)
            db.session.commit()

    def unfollow(self, user_id, post_id):
        self.notification_members_repository.delete_by_user_id_post_id(user_id, post_id)
        db.session.commit()

    def save_trigger(self, user_id, post_id):
        member = self.notification_members_repository.get_by_user_id_post_id(user_id, post_id)
        if member:
            new_trigger = NotificationTrigger(NotificationId=member.Id)
            db.session.add(new_trigger)
            db.session.commit()
            return True
        return False
