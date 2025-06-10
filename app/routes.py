from . import db
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from .models import User, Post, NotificationMembers
import random

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    users = User.query.all()
    if request.method == 'POST':
        user_id = int(request.form.get('user_id'))
        session['user_id'] = user_id
        flash('Đăng nhập thành công!', 'success')
        return redirect(url_for('main.index'))
    return render_template('login.html', users=users)

@main_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Đã đăng xuất!', 'success')
    return redirect(url_for('main.login'))

@main_bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post_detail(post_id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('main.login'))
    current_user = User.query.get(user_id)

    post = Post.query.get_or_404(post_id)
    post.ViewCount = (post.ViewCount or 0) + 1
    db.session.commit()

    price_error = None
    is_followed = False
    member = None

    if current_user:
        member = NotificationMembers.query.filter_by(UserId=current_user.Id, PostId=post.Id).first()
        is_followed = member is not None

    if request.method == 'POST':
        if 'price' in request.form:
            try:
                new_price = float(request.form.get('price'))
                if new_price <= 0:
                    price_error = "Giá phải lớn hơn 0"
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
                flash('Đã Follow!', 'success')
            else:
                NotificationMembers.query.filter_by(UserId=current_user.Id, PostId=post.Id).delete()
                db.session.commit()
                flash('Đã Unfollow!', 'success')
            return redirect(url_for('main.post_detail', post_id=post.Id))
        elif 'save' in request.form:
            if not is_followed:
                flash('Phải Follow trước khi Save!', 'danger')
            else:
                from .models import NotificationTrigger
                new_trigger = NotificationTrigger(NotificationId=member.Id)
                db.session.add(new_trigger)
                db.session.commit()
                flash('Đã trigger thông báo (Save) thành công!', 'success')
            return redirect(url_for('main.post_detail', post_id=post.Id))

    return render_template(
        'detail.html',
        post=post,
        user=current_user,
        price_error=price_error,
        is_followed=is_followed
    )

