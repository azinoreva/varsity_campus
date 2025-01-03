""" User model """

from .. import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
from flask_dance.contrib.google import make_google_blueprint
from datetime import datetime


# Define Roles
class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    users = db.relationship('User',
                            secondary='user_roles',
                            back_populates='roles')


# Many-to-Many table between Users and Roles
user_roles = db.Table(
    'user_roles',
    db.Column('user_id',
              db.Integer,
              db.ForeignKey('users.id'),
              primary_key=True),
    db.Column('role_id',
              db.Integer,
              db.ForeignKey('roles.id'),
              primary_key=True))


# OAuth Model
class UserOAuth(OAuthConsumerMixin, db.Model):
    __tablename__ = 'user_oauth'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='oauth', uselist=False)


# User Model with Roles and OAuth
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    profile_image = db.Column(db.String(200), default='default.jpg')
    bio = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # OAuth relationship
    oauth = db.relationship('UserOAuth', back_populates='user', uselist=False)

    # Relationships for roles, posts, messages, and communities
    roles = db.relationship('Role', secondary=user_roles, back_populates='users')
    messages = db.relationship('CommunityMessage', back_populates='user')
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='user', lazy='dynamic')
    sent_messages = db.relationship('Message',
                                    foreign_keys='Message.sender_id',
                                    backref='sender_user',
                                    lazy='dynamic')
    received_messages = db.relationship('Message',
                                        foreign_keys='Message.receiver_id',
                                        backref='receiver_user',
                                        lazy='dynamic')
    friends = db.relationship('User',
                              secondary='friends',
                              primaryjoin='User.id==friends.c.user_id',
                              secondaryjoin='User.id==friends.c.friend_id',
                              backref='friend_of',
                              lazy='dynamic')

    def __init__(self, username, email, password_hash, roles=None):
        self.username = username
        self.email = email
        self.password_hash = password_hash
        if roles is None:
            # Set default role to 'User' if no roles are provided
            default_role = Role.query.filter_by(name='User').first()
            if default_role:
                self.roles = [default_role]
            else:
                self.roles = []
        else:
            self.roles = roles

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Roles and Permissions
    def has_role(self, role_name):
        return any(role.name == role_name for role in self.roles)

    def assign_role(self, role):
        if not self.has_role(role.name):
            self.roles.append(role)

    def remove_role(self, role):
        if self.has_role(role.name):
            self.roles.remove(role)

    # Super Admin Functions
    def is_super_admin(self):
        return self.has_role('Super Admin')

    def assign_lecturer(self, user):
        if self.is_super_admin():
            lecturer_role = Role.query.filter_by(name='Lecturer').first()
            if lecturer_role:
                user.assign_role(lecturer_role)
            else:
                raise ValueError("Lecturer role does not exist.")

    def delete_post(self, post):
        if self.is_super_admin():
            db.session.delete(post)
            db.session.commit()


# Many-to-Many table for friends
friends = db.Table(
    'friends',
    db.Column('user_id',
              db.Integer,
              db.ForeignKey('users.id'),
              primary_key=True),
    db.Column('friend_id',
              db.Integer,
              db.ForeignKey('users.id'),
              primary_key=True))

# class FriendRequest(db.Model):
#     __tablename__ = 'friend_requests'
    
#     id = db.Column(db.Integer, primary_key=True)
#     sender_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#     receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#     accepted = db.Column(db.Boolean, default=False)

#     sender = db.relationship('User', foreign_keys=[sender_id])
#     receiver = db.relationship('User', foreign_keys=[receiver_id])