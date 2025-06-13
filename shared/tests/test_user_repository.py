from shared.models.user_model import User
from shared.repository.user_repository import UserRepository

def test_user_get_by_id(session):
    user = User(Name="Test", Email="test@example.com")
    session.add(user)
    session.commit()

    repo = UserRepository(session)
    result = repo.get_by_id(user.Id)
    assert result.Email == "test@example.com"

def test_user_get_all(session):
    session.add_all([
        User(Name="A", Email="a@example.com"),
        User(Name="B", Email="b@example.com"),
    ])
    session.commit()

    repo = UserRepository(session)
    results = repo.get_all()
    assert len(results) == 2
