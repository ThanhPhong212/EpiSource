import pytest
from flask_jwt_extended import create_access_token
from shared.models.post_model import Post
from shared.models.user_model import User

def seed_user(session):
    user = User(Name="Test", Email="test@example.com")
    session.add(user)
    session.commit()
    return user

def seed_post(session, title="Post A"):
    post = Post(Title=title, Description="Demo", Price=10000, ViewCount=0)
    session.add(post)
    session.commit()
    return post

@pytest.fixture
def access_token(app, session):
    user = seed_user(session)
    with app.app_context():
        return create_access_token(identity=str(user.Id))

def test_index_route(client, session, access_token):
    post = seed_post(session)
    res = client.get("/posts/", headers={"Authorization": f"Bearer {access_token}"})
    assert res.status_code == 200
    assert post.Title in res.get_data(as_text=True)

def test_post_detail_requires_login(client, session):
    post = seed_post(session)
    res = client.get(f"/posts/{post.Id}")
    assert res.status_code == 401

def test_post_detail_get_logged_in(client, session, access_token):
    post = seed_post(session)
    res = client.get(f"/posts/{post.Id}", headers={"Authorization": f"Bearer {access_token}"})
    assert res.status_code == 200
    assert post.Title in res.get_data(as_text=True)

def test_post_detail_follow_post(client, session, access_token):
    post = seed_post(session)
    res = client.post(f"/posts/{post.Id}/follow", json={"user_id": 1}, headers={"Authorization": f"Bearer {access_token}"})
    assert res.status_code == 200
    assert res.get_json()["status"] == "success"

def test_post_detail_price_update_valid(client, session, access_token):
    post = seed_post(session)
    res = client.post(f"/posts/{post.Id}/price", json={"price": 120000}, headers={"Authorization": f"Bearer {access_token}"})
    assert res.status_code == 200
    assert "updated" in res.get_json()["message"].lower()

def test_post_detail_price_update_invalid(client, session, access_token):
    post = seed_post(session)
    res = client.post(f"/posts/{post.Id}/price", json={"price": -1000}, headers={"Authorization": f"Bearer {access_token}"})
    assert res.status_code == 400
    assert "price must be greater" in res.get_json()["message"].lower()
