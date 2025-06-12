from flask import session, flash, redirect, url_for, render_template, request

class PostService:
    def __init__(self, post_repository):
        self.post_repository = post_repository
