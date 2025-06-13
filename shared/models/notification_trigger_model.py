from shared.db import db

class NotificationTrigger(db.Model):
    __tablename__ = 'NotificationTrigger'
    Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    NotificationId = db.Column(db.Integer, db.ForeignKey('NotificationMembers.Id', ondelete="CASCADE"))

