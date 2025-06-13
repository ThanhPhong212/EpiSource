from shared.models.notification_trigger_model import NotificationTrigger
from shared.repository.notification_trigger_repository import NotificationTriggerRepository

def test_get_all_triggers(session):
    trigger1 = NotificationTrigger(NotificationId=101)
    trigger2 = NotificationTrigger(NotificationId=102)
    session.add_all([trigger1, trigger2])
    session.commit()

    repo = NotificationTriggerRepository(session)
    results = repo.get_all()

    assert len(results) == 2
    ids = [t.NotificationId for t in results]
    assert 101 in ids
    assert 102 in ids
