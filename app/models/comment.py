"""Comment model for posts"""
from datetime import datetime
from .. import db

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign Keys
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)  # Links to the Post model
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Links to the User model

    # Relationship Fields
    likes = db.relationship('CommentLike', backref='comment', lazy=True)
    dislikes = db.relationship('CommentDislike', backref='comment', lazy=True)
    reposts = db.relationship('CommentRepost', backref='comment', lazy=True)

    def __init__(self, content, post_id, user_id):
        self.content = content
        self.post_id = post_id
        self.user_id = user_id


class CommentLike(db.Model):
    __tablename__ = 'comment_likes'

    id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, comment_id, user_id):
        self.comment_id = comment_id
        self.user_id = user_id


class CommentDislike(db.Model):
    __tablename__ = 'comment_dislikes'

    id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, comment_id, user_id):
        self.comment_id = comment_id
        self.user_id = user_id


class CommentRepost(db.Model):
    __tablename__ = 'comment_reposts'

    id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, comment_id, user_id):
        self.comment_id = comment_id
        self.user_id = user_id
