from dotenv import load_dotenv
load_dotenv()

import sys
import os
import random
import time
import logging
import yagmail
from reportlab.pdfgen import canvas
from app import create_app, db
from app.models import User, Post, NotificationMembers, NotificationTrigger

# --- Cấu hình logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

# --- Cấu hình đường dẫn ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'email_templates')

# --- Cấu hình email ---
GMAIL_USER = os.environ.get("GMAIL_USER")
GMAIL_PASS = os.environ.get("GMAIL_PASS")
print("GMAIL_USER:", GMAIL_USER)  # Debugging line to check GMAIL_USER

if not GMAIL_USER or not GMAIL_PASS:
    logging.error("Thiếu thông tin tài khoản Gmail trong biến môi trường.")
    sys.exit(1)

app = create_app()

def create_pdf(post, filename):
    """Tạo file PDF chứa thông tin bài đăng."""
    c = canvas.Canvas(filename)
    c.drawString(50, 800, "Thông tin Post")
    c.drawString(50, 780, f"Title: {post.Title}")
    c.drawString(50, 760, f"Description: {post.Description}")
    c.drawString(50, 740, f"Price: {post.Price}")
    c.save()

def render_email_template(user, post):
    """Render nội dung email từ template HTML."""
    template_file = os.path.join(
        TEMPLATE_DIR,
        random.choice(['template1.html', 'template2.html', 'template3.html'])
    )
    with open(template_file, encoding='utf-8') as f:
        html = f.read()
    html = html.replace('{{ user_name }}', user.Name)
    html = html.replace('{{ post_title }}', post.Title)
    html = html.replace('{{ post_desc }}', post.Description or '')
    html = html.replace('{{ post_price }}', str(post.Price or ''))
    return html

def send_notification_email(yag, user, post):
    """Gửi email thông báo kèm file PDF."""
    pdf_file = f"post_{post.Id}.pdf"
    try:
        create_pdf(post, pdf_file)
        subject = f"Notification for post {post.Title}"
        content = render_email_template(user, post)
        yag.send(user.Email, subject, contents=content, attachments=pdf_file)
        logging.info(f"Đã gửi email cho {user.Email} về post {post.Title}")
    except Exception as e:
        logging.error(f"Lỗi khi gửi email cho {user.Email}: {e}")
    finally:
        if os.path.exists(pdf_file):
            os.remove(pdf_file)

def process_triggers():
    """Xử lý các trigger gửi thông báo."""
    with app.app_context():
        triggers = NotificationTrigger.query.all()
        for trig in triggers:
            try:
                notif = db.session.get(NotificationMembers, trig.NotificationId)
                if not notif:
                    continue
                user = db.session.get(User, notif.UserId)
                post = db.session.get(Post, notif.PostId)
                if user and post:
                    send_notification_email(yag, user, post)
                db.session.delete(trig)
                db.session.commit()
            except Exception as e:
                logging.error(f"Lỗi khi xử lý trigger {trig.NotificationId}: {e}")
                db.session.rollback()

def main():
    global yag
    yag = yagmail.SMTP(GMAIL_USER, GMAIL_PASS)
    logging.info("Worker started.")
    while True:
        process_triggers()
        time.sleep(3)

if __name__ == '__main__':
    main()
