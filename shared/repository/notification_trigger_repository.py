from shared.models.notification_trigger_model import NotificationTrigger

class NotificationTriggerRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    def get_all(self):
        triggers = self.db_session.query(NotificationTrigger).all()
        return triggers
