import sys
import os
import time
import logging
from dotenv import load_dotenv
import yagmail

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'background_service/email_templates')
print(f"TEMPLATE_DIR: {TEMPLATE_DIR}")
from shared.db import db
from shared.models import User, Post, NotificationMembers
from shared.repository import NotificationTriggerRepository
from web_app import create_app
from background_service.email_sender import send_notification_email
from background_service.file_helper import create_pdf

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

load_dotenv()
GMAIL_USER = os.environ.get("GMAIL_USER")
GMAIL_PASS = os.environ.get("GMAIL_PASS")

notification_trigger_repository = NotificationTriggerRepository(db.session)
app = create_app()

if not GMAIL_USER or not GMAIL_PASS:
    logging.error("Thiếu thông tin tài khoản Gmail trong biến môi trường.")
    sys.exit(1)

def process_triggers(yag):
    with app.app_context():
        triggers = notification_trigger_repository.get_all()
        for trig in triggers:
            try:
                notif = db.session.get(NotificationMembers, trig.NotificationId)
                if not notif:
                    continue
                user = db.session.get(User, notif.UserId)
                post = db.session.get(Post, notif.PostId)
                if user and post:
                    pdf_file = f"post_{post.Id}.pdf"
                    send_notification_email(
                        yag, user, post, TEMPLATE_DIR, pdf_file, create_pdf
                    )
                    logging.info(f"Đã gửi email cho {user.Email} về post {post.Title}")
                db.session.delete(trig)
                db.session.commit()
            except Exception as e:
                logging.error(f"Lỗi khi xử lý trigger {trig.NotificationId}: {e}")
                db.session.rollback()

def main():
    yag = yagmail.SMTP(GMAIL_USER, GMAIL_PASS)
    logging.info("Worker started.")
    while True:
        process_triggers(yag)
        time.sleep(3)

if __name__ == '__main__':
    main()
