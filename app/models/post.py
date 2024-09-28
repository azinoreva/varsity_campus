from datetime import datetime
from .. import db

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(2000), nullable=True)  # Text limited to 2000 characters
    image = db.Column(db.String(255), nullable=True)  # Store image path
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    likes = db.relationship('Like', backref='post', lazy=True)  # Likes for the post
    comments = db.relationship('Comment', backref='post', lazy=True)  # Comments on the post
    reposts = db.relationship('Repost', backref='post', lazy=True)  # Reposts
    views = db.Column(db.Integer, default=0)  # Number of views

    def save_post(self):
        db.session.add(self)
        db.session.commit()

class Like(db.Model):
    __tablename__ = 'likes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)  # Comment limited to 500 characters
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

class Repost(db.Model):
    __tablename__ = 'reposts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

    def save_repost(self):
        db.session.add(self)
        db.session.commit()
