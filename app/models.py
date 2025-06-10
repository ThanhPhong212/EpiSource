from . import db

class User(db.Model):
    __tablename__ = 'User'
    Id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=False)
    Email = db.Column(db.String(100), unique=True, nullable=False)

class Post(db.Model):
    __tablename__ = 'Post'
    Id = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(200), nullable=False)
    Description = db.Column(db.Text)
    Price = db.Column(db.Numeric(10,2))
    ViewCount = db.Column(db.Integer, default=0)

class NotificationMembers(db.Model):
    __tablename__ = 'NotificationMembers'
    Id = db.Column(db.Integer, primary_key=True)
    UserId = db.Column(db.Integer, db.ForeignKey('User.Id', ondelete="CASCADE"))
    PostId = db.Column(db.Integer, db.ForeignKey('Post.Id', ondelete="CASCADE"))

class NotificationTrigger(db.Model):
    __tablename__ = 'NotificationTrigger'
    Id = db.Column(db.Integer, primary_key=True)
    NotificationId = db.Column(db.Integer, db.ForeignKey('NotificationMembers.Id', ondelete="CASCADE"))
