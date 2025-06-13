import pytest
from flask import session
from shared.models.post_model import Post
from shared.models.user_model import User


def seed_post(session, title="Test Post", price=50000):
    post = Post(Title=title, Description="Test Desc", Price=price, ViewCount=0)
    session.add(post)
    session.commit()
    return post


def seed_user(session, name="Test User", email="test@example.com"):
    user = User(Name=name, Email=email)
    session.add(user)
    session.commit()
    return user


def test_index_route(client, session):
    post = seed_post(session)

    res = client.get("/posts/")
    assert res.status_code == 200
    assert post.Title in res.get_data(as_text=True)


def test_post_detail_requires_login(client, session):
    post = seed_post(session)

    res = client.get(f"/posts/{post.Id}", follow_redirects=True)
    assert res.status_code == 200
    assert "đăng nhập" in res.get_data(as_text=True).lower()


def test_post_detail_get_logged_in(client, session):
    post = seed_post(session)
    user = seed_user(session)

    with client.session_transaction() as sess:
        sess['user_id'] = user.Id

    res = client.get(f"/posts/{post.Id}")
    assert res.status_code == 200
    assert post.Title in res.get_data(as_text=True)


def test_post_detail_follow_post(client, session):
    post = seed_post(session)
    user = seed_user(session)

    with client.session_transaction() as sess:
        sess['user_id'] = user.Id

    res = client.post(f"/posts/{post.Id}", data={"follow": "1"}, follow_redirects=True)
    assert res.status_code == 200
    assert "đã follow" in res.get_data(as_text=True).lower()


def test_post_detail_price_update_valid(client, session):
    post = seed_post(session)
    user = seed_user(session)

    with client.session_transaction() as sess:
        sess['user_id'] = user.Id

    res = client.post(f"/posts/{post.Id}", data={"price": "123456"}, follow_redirects=True)
    assert res.status_code == 200
    assert "cập nhật giá" in res.get_data(as_text=True).lower()


def test_post_detail_price_update_invalid(client, session):
    post = seed_post(session)
    user = seed_user(session)

    with client.session_transaction() as sess:
        sess['user_id'] = user.Id

    res = client.post(f"/posts/{post.Id}", data={"price": "-5000"}, follow_redirects=True)
    assert res.status_code == 200
    assert "giá phải lớn hơn" in res.get_data(as_text=True).lower()
