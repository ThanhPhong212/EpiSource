import sys
import os
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'email_templates')

import time
import yagmail
from reportlab.pdfgen import canvas
from app import create_app, db
from app.models import User, Post, NotificationMembers, NotificationTrigger

app = create_app()

# --- Cấu hình email ---
GMAIL_USER = os.environ.get("GMAIL_USER")
GMAIL_PASS = os.environ.get("GMAIL_PASS")

def create_pdf(post, filename):
    c = canvas.Canvas(filename)
    c.drawString(50, 800, f"Thông tin Post")
    c.drawString(50, 780, f"Title: {post.Title}")
    c.drawString(50, 760, f"Description: {post.Description}")
    c.drawString(50, 740, f"Price: {post.Price}")
    c.save()

def render_email_template(user, post):
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

def main():
    yag = yagmail.SMTP(GMAIL_USER, GMAIL_PASS)
    print("Worker started.")
    while True:
        with app.app_context():
            triggers = NotificationTrigger.query.all()
            for trig in triggers:
                notif = db.session.get(NotificationMembers, trig.NotificationId)
                if notif:
                    user = db.session.get(User, notif.UserId)
                    post = db.session.get(Post, notif.PostId)       
                    if user and post:
                        # Tạo file PDF tạm
                        pdf_file = f"post_{post.Id}.pdf"
                        create_pdf(post, pdf_file)
                        subject = f"Notification for post {post.Title}"
                        content = render_email_template(user, post)
                        try:
                            yag.send(user.Email, subject, contents=content, attachments=pdf_file)
                            print(f"Đã gửi email cho {user.Email} về post {post.Title}")
                        except Exception as e:
                            print("Gửi email lỗi:", e)
                        # Xóa trigger đã gửi xong để không gửi lại nữa
                        db.session.delete(trig)
                        db.session.commit()
        time.sleep(3)

if __name__ == '__main__':
    main()
