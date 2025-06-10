# EpiSource Python Demo Project

## Mục tiêu

Demo hệ thống quản lý bài post, user, theo dõi (follow), notification và gửi email có file PDF đính kèm với worker chạy nền.

---

## 1. Yêu cầu hệ thống

- Python 3.10+
- PostgreSQL (có thể chạy bằng Docker)
- Thư viện: Flask, Flask-SQLAlchemy, python-dotenv, yagmail, reportlab, psycopg2-binary

---

## 2. Cài đặt môi trường

### 2.1. Clone project & tạo virtual environment

```bash
git clone <repo_url>
cd EpiSource
python -m venv venv
venv\Scripts\activate       # Windows
# source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt

# background
venv\Scripts\activate 
python background/worker.py