from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from web_app.observers import on_user_follow, on_post_save, on_trigger_create
from shared.db import db
from shared.models import NotificationMembers, NotificationTrigger
from shared.repository import UserRepository, PostRepository, NotificationMembersRepository, NotificationTriggerRepository
from .services.auth_service import AuthService
from .services.post_service import PostService

main_bp = Blueprint('main', __name__)

# Inject dependencies
user_repository = UserRepository(db.session)
post_repository = PostRepository(db.session)
notification_members_repository = NotificationMembersRepository(db.session)
notification_trigger_repository = NotificationTriggerRepository(db.session)
auth_service = AuthService(user_repository)
post_service = PostService(post_repository)

@main_bp.route('/')
def index():
    posts = post_repository.get_all()
    return render_template('index.html', posts=posts)

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    users = user_repository.get_all()
    if request.method == 'POST':
        user_id = int(request.form.get('user_id'))
        return auth_service.login(user_id)
    return render_template('login.html', users=users)

@main_bp.route('/logout')
def logout():
    return auth_service.logout()

@main_bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post_detail(post_id):
    user_id = session.get('user_id')
    if not user_id:
        flash('Bạn cần đăng nhập để xem chi tiết bài viết.', 'warning')
        return redirect(url_for('main.login'))
    current_user = user_repository.get_by_id(user_id)
    if not current_user:
        session.pop('user_id', None)
        flash('Tài khoản không hợp lệ, vui lòng đăng nhập lại.', 'danger')
        return redirect(url_for('main.login'))

    post = post_repository.get_by_id(post_id)
    post.ViewCount = (post.ViewCount or 0) + 1
    db.session.commit()

    price_error = None
    member = notification_members_repository.get_by_user_id_post_id(current_user.Id, post.Id)
    is_followed = member is not None

    if request.method == 'POST':
        if 'price' in request.form:
            try:
                new_price = float(request.form.get('price'))
                if new_price <= 0 or new_price >= 1e8:
                    price_error = "Giá phải lớn hơn 0 và nhỏ hơn 100,000,000"
                else:
                    post.Price = new_price
                    db.session.commit()
                    flash("Cập nhật giá thành công!", "success")
                    return redirect(url_for('main.post_detail', post_id=post.Id))
            except Exception:
                price_error = "Giá không hợp lệ!"
        elif 'follow' in request.form:
            if not is_followed:
                new_member = NotificationMembers(UserId=current_user.Id, PostId=post.Id)
                db.session.add(new_member)
                db.session.commit()
                on_user_follow.notify(current_user, post)  # Gọi event khi follow
                flash('Đã Follow!', 'success')
            else:
                db.session.query(NotificationMembers).filter_by(UserId=current_user.Id, PostId=post.Id).delete()
                db.session.commit()
                flash('Đã Unfollow!', 'success')
            return redirect(url_for('main.post_detail', post_id=post.Id))
        elif 'save' in request.form:
            if not is_followed:
                flash('Bạn cần Follow trước khi Save!', 'danger')
            else:
                member = db.session.query(NotificationMembers).filter_by(UserId=current_user.Id, PostId=post.Id).first()
                if member:
                    new_trigger = NotificationTrigger(NotificationId=member.Id)
                    db.session.add(new_trigger)
                    db.session.commit()
                    on_post_save.notify(post, current_user)
                    on_trigger_create.notify(current_user, post)
                    flash('Đã trigger thông báo (Save) thành công!', 'success')
                else:
                    flash('Không tìm thấy thông tin Follow!', 'danger')
            return redirect(url_for('main.post_detail', post_id=post.Id))

    return render_template(
        'detail.html',
        post=post,
        user=current_user,
        price_error=price_error,
        is_followed=is_followed
    )

