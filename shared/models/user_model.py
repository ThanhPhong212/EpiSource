from shared.db import db, Base

class User(db.Model):
    __tablename__ = 'User'
    Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(100), nullable=False)
    Email = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"Id: {self.Id}, Name: {self.Name}, Email: {self.Email}"
