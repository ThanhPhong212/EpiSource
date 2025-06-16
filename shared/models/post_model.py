from shared.db import db
from decimal import Decimal
class Post(db.Model):
    __tablename__ = 'Post'
    Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Title = db.Column(db.String(200), nullable=False, unique=True)
    Description = db.Column(db.Text)
    Price = db.Column(db.Numeric(10,2))
    ViewCount = db.Column(db.Integer, default=0)

    def to_dict(self):
       return {
           "id": self.Id,
           "title": self.Title,
           "description": self.Description,
           "price": float(self.Price) if self.Price is not None else 0,
           "view_count": self.ViewCount or 0
       }

    def __repr__(self):
        return f"Id: {self.Id}, Title: {self.Title}, Description: {self.Description}, Price: {self.Price}, ViewCount: {self.ViewCount}"