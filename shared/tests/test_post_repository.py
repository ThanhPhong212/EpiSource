from shared.models.post_model import Post
from shared.repository.post_repository import PostRepository

def test_get_by_id(session):
    post = Post(Title="Test Post", Description="Demo", Price=50000, ViewCount=0)
    session.add(post)
    session.commit()

    repo = PostRepository(session)
    result = repo.get_by_id(post.Id)

    assert result is not None
    assert result.Title == "Test Post"
    assert result.Price == 50000


def test_get_all(session):
    session.add_all([
        Post(Title="Post A", Description="A", Price=10000, ViewCount=0),
        Post(Title="Post B", Description="B", Price=20000, ViewCount=0),
    ])
    session.commit()

    repo = PostRepository(session)
    results = repo.get_all()

    assert isinstance(results, list)
    assert len(results) == 2
    titles = [p.Title for p in results]
    assert "Post A" in titles
    assert "Post B" in titles
