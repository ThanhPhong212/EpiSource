from flask_restx import Namespace, Resource, fields
from flask import request
from shared.db import db
from shared.repository import (
    PostRepository, NotificationMembersRepository, NotificationTriggerRepository
)
from web_app.services.post_service import PostService
from flask_jwt_extended import jwt_required

api = Namespace('post', path='/posts', description='Post APIs')

price_model = api.model('UpdatePrice', {
    'price': fields.Float(required=True, description='New price')
})

follow_model = api.model('UserAction', {
    'user_id': fields.Integer(required=True, description='User ID')
})


def get_post_service():
    post_repo = PostRepository(db.session)
    notif_repo = NotificationMembersRepository(db.session)
    trigger_repo = NotificationTriggerRepository(db.session)
    return PostService(post_repo, notif_repo, trigger_repo)

@api.route('/')
class PostList(Resource):
    @jwt_required()
    @api.doc(description="Get all posts")
    def get(self):
        service = get_post_service()
        posts = service.get_all()
        return {"status": "success", "data": [p.to_dict() for p in posts]}


@api.route('/<int:post_id>')
class PostDetail(Resource):
    @jwt_required()
    @api.doc(description="Get post details and increase view count")
    def get(self, post_id):
        service = get_post_service()
        post = service.get_by_id(post_id)
        if not post:
            return {"status": "error", "message": "Post not found"}, 404

        service.increase_view_count(post)
        return {"status": "success", "data": post.to_dict()}

@api.route('/<int:post_id>/price')
class UpdatePrice(Resource):
    @jwt_required()
    @api.expect(price_model)
    @api.doc(description="Update post price")
    def post(self, post_id):
        service = get_post_service()
        post = service.get_by_id(post_id)
        if not post:
            return {"status": "error", "message": "Post not found"}, 404

        data = request.get_json()
        price = data.get('price')
        if not price or price <= 0 or price >= 1e8:
            return {"status": "error", "message": "Price must be greater than 0 and less than 100,000,000"}, 400

        service.update_price(post, price)
        return {"status": "success", "message": "Price updated successfully!"}

@api.route('/<int:post_id>/follow')
class FollowPost(Resource):
    @jwt_required()
    @api.expect(follow_model)
    @api.doc(description="Follow post")
    def post(self, post_id):
        user_id = request.get_json().get('user_id')
        if not user_id:
            return {"status": "error", "message": "Missing user_id"}, 400

        service = get_post_service()
        service.follow(user_id, post_id)
        return {"status": "success", "message": "Post followed successfully!"}

@api.route('/<int:post_id>/unfollow')
class UnfollowPost(Resource):
    @jwt_required()
    @api.expect(follow_model)
    @api.doc(description="Unfollow post")
    def post(self, post_id):
        user_id = request.get_json().get('user_id')
        if not user_id:
            return {"status": "error", "message": "Missing user_id"}, 400

        service = get_post_service()
        service.unfollow(user_id, post_id)
        return {"status": "success", "message": "Post unfollowed successfully!"}

@api.route('/<int:post_id>/save')
class SaveTrigger(Resource):
    @jwt_required()
    @api.expect(follow_model)
    @api.doc(description="Trigger notification for post (requires follow)")
    def post(self, post_id):
        user_id = request.get_json().get('user_id')
        if not user_id:
            return {"status": "error", "message": "Missing user_id"}, 400

        service = get_post_service()
        if service.save_trigger(user_id, post_id):
            return {"status": "success", "message": "Notification triggered successfully!"}
        return {"status": "error", "message": "You need to follow the post before triggering notifications!"}, 400
