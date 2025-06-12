from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from shared.repository import (
    PostRepository, NotificationMembersRepository, NotificationTriggerRepository
)
from shared.db import db
from web_app.services.post_service import PostService
from shared.repository import UserRepository

post_bp = Blueprint('post', __name__, url_prefix="/posts")

def get_post_service():
    post_repo = PostRepository(db.session)
    notif_repo = NotificationMembersRepository(db.session)
    trigger_repo = NotificationTriggerRepository(db.session)
    return PostService(post_repo, notif_repo, trigger_repo)


@post_bp.route('/')
def index():
    service = get_post_service()
    posts = service.get_all()
    return render_template('index.html', posts=posts)


@post_bp.route('/<int:post_id>', methods=['GET', 'POST'])
def post_detail(post_id):
    user_repo = UserRepository(db.session)
    user_id = session.get('user_id')
    if not user_id:
        flash('Bạn cần đăng nhập!', 'warning')
        return redirect(url_for('auth.login'))
    
    user = user_repo.get_by_id(user_id)
    service = get_post_service()
    post = service.get_by_id(post_id)

    if not post:
        flash('Bài viết không tồn tại!', 'danger')
        return redirect(url_for('post.index'))

    service.increase_view_count(post)
    price_error = None
    is_followed = service.is_followed(user_id, post_id)

    if request.method == 'POST':
        form = request.form

        if 'price' in form:
            try:
                new_price = float(form.get('price'))
                if new_price <= 0 or new_price >= 1e8:
                    price_error = "Giá phải lớn hơn 0 và nhỏ hơn 100,000,000"
                else:
                    service.update_price(post, new_price)
                    flash("Cập nhật giá thành công!", "success")
                    return redirect(url_for('post.post_detail', post_id=post.Id))
            except Exception:
                price_error = "Giá không hợp lệ!"

        elif 'follow' in form:
            service.follow(user_id, post_id)
            flash('Đã Follow!', 'success')
            return redirect(url_for('post.post_detail', post_id=post.Id))

        elif 'unfollow' in form:
            service.unfollow(user_id, post_id)
            flash('Đã Unfollow!', 'success')
            return redirect(url_for('post.post_detail', post_id=post.Id))

        elif 'save' in form:
            ok = service.save_trigger(user_id, post_id)
            if ok:
                flash('Đã trigger thông báo (Save) thành công!', 'success')
            else:
                flash('Bạn cần Follow trước khi Save!', 'danger')
            return redirect(url_for('post.post_detail', post_id=post.Id))

    return render_template(
        'detail.html',
        post=post,
        user=user,
        price_error=price_error,
        is_followed=is_followed
    )
