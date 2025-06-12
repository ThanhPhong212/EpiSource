from sqlalchemy.dialects.postgresql import insert
from shared.models import User
from shared.models import Post

class Seed:
    def __init__(self, db_session):
        self.db_session = db_session

    def start(self):
        self.__seed_users()
        self.__seed_posts()

    def __seed_users(self):
        users = [
            User(Name="User1", Email="user1@example.com"),
            User(Name="User2", Email="user2@example.com"),
            User(Name="User3", Email="user3@example.com")
        ]

        try:
            for user in users:
                stmt = insert(User).values(Name=user.Name, Email=user.Email)
                stmt = stmt.on_conflict_do_nothing(index_elements=['Email'])
                self.db_session.execute(stmt)
            self.db_session.flush()
            self.db_session.commit()
            print("Seed users successfully added!")
        except Exception as e:
            self.db_session.rollback()
            print(f"Error seeding users: {e}")

    def __seed_posts(self):
        posts = [
            Post(Title="post1", Description="description1", Price=100, ViewCount=0),
            Post(Title="post2", Description="description2", Price=105, ViewCount=0),
            Post(Title="post3", Description="description3", Price=50, ViewCount=0),
            Post(Title="post4", Description="description4", Price=200, ViewCount=0),
            Post(Title="post5", Description="description5", Price=500, ViewCount=0),
            Post(Title="post6", Description="description6", Price=250, ViewCount=0),
            Post(Title="post7", Description="description7", Price=200, ViewCount=0),
            Post(Title="post8", Description="description8", Price=100, ViewCount=0),
            Post(Title="post9", Description="description9", Price=300, ViewCount=0),
            Post(Title="post10", Description="description10", Price=110, ViewCount=0)
        ]

        try:
            for post in posts:
                stmt = insert(Post).values(Title=post.Title, Description=post.Description, Price=post.Price)
                stmt = stmt.on_conflict_do_nothing(index_elements=['Title'])
                self.db_session.execute(stmt)
            self.db_session.flush()
            self.db_session.commit()
            print("Seed posts successfully added!")
        except Exception as e:
            self.db_session.rollback()
            print(f"Error seeding posts: {e}")
