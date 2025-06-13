import sys
import os
import pytest
import pathlib
import importlib
from unittest.mock import patch, MagicMock
from shared.models import User, Post, NotificationMembers, NotificationTrigger

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from shared.models import User, Post, NotificationMembers
from background_service.email_sender import render_email_template

# ----------------- FIXTURE -----------------

@pytest.fixture
def user():
    return User(Id=1, Name="Test User", Email="test@example.com")

@pytest.fixture
def post():
    return Post(Id=1, Title="Test Post", Description="Test Desc", Price=12345)

@pytest.fixture
def notif(user, post, session):
    notif = NotificationMembers(Id=1, UserId=user.Id, PostId=post.Id)
    session.add_all([user, post, notif])
    session.commit()
    return notif

# ----------------- TEST TEMPLATE -----------------
@pytest.mark.parametrize("filename", ["template1.html", "template2.html", "template3.html"])
@patch("background_service.email_sender.random.choice")
def test_render_email_template(mock_choice, user, post, filename):
    mock_choice.return_value = filename

    template_dir = pathlib.Path(__file__).parent.parent / "email_templates"
    assert template_dir.exists(), f"Không tìm thấy folder: {template_dir}"
    template_path = template_dir / filename
    assert template_path.exists(), f"Thiếu template: {filename}"

    content = render_email_template(user, post, template_dir)

    assert "Test User" in content
    assert "Test Post" in content
    assert "12345" in content

# ----------------- TEST TRIGGER -----------------
def test_process_triggers(session, user, post, notif):
    from background_service import worker
    importlib.reload(worker)

    trigger = NotificationTrigger(Id=1, NotificationId=notif.Id)

    with patch("background_service.worker.NotificationTriggerRepository.get_all", return_value=[trigger]), \
         patch("background_service.worker.db.session.get") as mock_get, \
         patch("background_service.worker.send_notification_email") as mock_send_email, \
         patch("background_service.worker.os.path.exists", return_value=True), \
         patch("background_service.worker.os.remove"):

        mock_get.side_effect = lambda model, id_: {
            NotificationMembers: notif,
            User: user,
            Post: post
        }.get(model)

        with worker.app.app_context():
            worker.process_triggers(MagicMock())

        mock_send_email.assert_called_once()