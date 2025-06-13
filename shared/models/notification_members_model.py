from shared.db import db

class NotificationMembers(db.Model):
    __tablename__ = 'NotificationMembers'
    Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserId = db.Column(db.Integer, db.ForeignKey('User.Id', ondelete="CASCADE"))
    PostId = db.Column(db.Integer, db.ForeignKey('Post.Id', ondelete="CASCADE"))
