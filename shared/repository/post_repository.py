from shared.models.post_model import Post

class PostRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    def get_by_id(self, post_id):
        post = self.db_session.query(Post).filter_by(Id=post_id).first()
        return post

    def get_all(self):
        posts = self.db_session.query(Post).all()
        return posts
