from shared.models.notification_members_model import NotificationMembers
from shared.repository.notification_members_repository import NotificationMembersRepository

def test_get_by_user_id_post_id(session):
    # Không set Id thủ công
    member = NotificationMembers(UserId=1, PostId=1)
    session.add(member)
    session.commit()

    repo = NotificationMembersRepository(session)
    result = repo.get_by_user_id_post_id(user_id=1, post_id=1)

    assert result is not None
    assert result.UserId == 1
    assert result.PostId == 1

def test_get_all_members(session):
    session.add_all([
        NotificationMembers(UserId=1, PostId=1),
        NotificationMembers(UserId=2, PostId=2),
    ])
    session.commit()

    repo = NotificationMembersRepository(session)
    results = repo.get_all()

    assert isinstance(results, list)
    assert len(results) == 2
    user_ids = {m.UserId for m in results}
    assert 1 in user_ids
    assert 2 in user_ids
