import pytest
from web_app.services.post_service import PostService
from shared.models import Post, NotificationMembers, NotificationTrigger


# --- Dummy Post object ---
@pytest.fixture
def dummy_post():
    return Post(Id=1, Title="Test Post", Description="Test", Price=1000, ViewCount=0)


# --- Mock Repositories ---
class MockPostRepo:
    def __init__(self):
        self.posts = [Post(Id=1, Title="Test Post", Description="...", Price=1000, ViewCount=0)]

    def get_all(self):
        return self.posts

    def get_by_id(self, post_id):
        return next((p for p in self.posts if p.Id == post_id), None)


class MockMemberRepo:
    def __init__(self):
        self.members = []

    def get_by_user_id_post_id(self, user_id, post_id):
        return next((m for m in self.members if m.UserId == user_id and m.PostId == post_id), None)

    def delete_by_user_id_post_id(self, user_id, post_id):
        self.members = [m for m in self.members if not (m.UserId == user_id and m.PostId == post_id)]

    def add_member(self, user_id, post_id):
        member = NotificationMembers(Id=len(self.members)+1, UserId=user_id, PostId=post_id)
        self.members.append(member)
        return member


class MockTriggerRepo:
    def __init__(self):
        self.triggers = []

    def add_trigger(self, notification_id):
        trigger = NotificationTrigger(Id=len(self.triggers)+1, NotificationId=notification_id)
        self.triggers.append(trigger)
        return trigger


# --- Fixture tạo service và monkeypatch session ---
@pytest.fixture
def service(monkeypatch):
    post_repo = MockPostRepo()
    member_repo = MockMemberRepo()
    trigger_repo = MockTriggerRepo()

    # Patch session.add
    def mock_add(obj):
        if isinstance(obj, NotificationMembers):
            member_repo.add_member(obj.UserId, obj.PostId)
        elif isinstance(obj, NotificationTrigger):
            trigger_repo.add_trigger(obj.NotificationId)

    monkeypatch.setattr("shared.db.db.session.add", mock_add)
    monkeypatch.setattr("shared.db.db.session.commit", lambda: None)

    return PostService(post_repo, member_repo, trigger_repo)


# --- Tests ---
def test_get_all_posts(service):
    posts = service.get_all()
    assert len(posts) == 1
    assert posts[0].Title == "Test Post"


def test_increase_view_count(service):
    post = service.get_by_id(1)
    assert post.ViewCount == 0
    service.increase_view_count(post)
    assert post.ViewCount == 1


def test_follow_and_is_followed(service):
    user_id = 10
    post_id = 1
    assert not service.is_followed(user_id, post_id)
    service.follow(user_id, post_id)
    assert service.is_followed(user_id, post_id)


def test_unfollow(service):
    user_id = 20
    post_id = 1
    service.follow(user_id, post_id)
    assert service.is_followed(user_id, post_id)
    service.unfollow(user_id, post_id)
    assert not service.is_followed(user_id, post_id)


def test_save_trigger(service):
    user_id = 99
    post_id = 1
    # Chưa follow → không trigger được
    assert not service.save_trigger(user_id, post_id)

    # Sau khi follow → trigger OK
    service.follow(user_id, post_id)
    assert service.save_trigger(user_id, post_id)
