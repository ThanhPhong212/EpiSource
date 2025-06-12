import os
import random

def render_email_template(user, post, template_dir):
    template_file = os.path.join(
        template_dir,
        random.choice(['template1.html', 'template2.html', 'template3.html'])
    )
    with open(template_file, encoding='utf-8') as f:
        html = f.read()
    html = html.replace('{{ user_name }}', user.Name)
    html = html.replace('{{ post_title }}', post.Title)
    html = html.replace('{{ post_desc }}', post.Description or '')
    html = html.replace('{{ post_price }}', str(post.Price or ''))
    return html

def send_notification_email(yag, user, post, template_dir, pdf_file, create_pdf_func):
    """Gửi email thông báo kèm file PDF."""
    try:
        create_pdf_func(post, pdf_file)
        subject = f"Notification for post {post.Title}"
        content = render_email_template(user, post, template_dir)
        yag.send(user.Email, subject, contents=content, attachments=pdf_file)
    finally:
        if os.path.exists(pdf_file):
            os.remove(pdf_file)
