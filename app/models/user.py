""" User model """

from .. import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
from flask_dance.contrib.google import make_google_blueprint


# Define Roles
class Role(db.Model):
  __tablename__ = 'roles'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50), unique=True, nullable=False)

  # Relationship between roles and users
  users = db.relationship('User',
                          secondary='user_roles',
                          back_populates='roles')


# Many-to-Many Table between Users and Roles
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


class UserOAuth(OAuthConsumerMixin, db.Model):
  __tablename__ = 'user_oauth'

  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  user = db.relationship('User', backref=db.backref('oauth', uselist=False))


# Extended User Model with OAuth and Roles
class User(UserMixin, db.Model):
  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(64), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password_hash = db.Column(db.String(128), nullable=False)
  profile_image = db.Column(db.String(200), default='default.jpg')
  bio = db.Column(db.String(200), nullable=True)
  created_at = db.Column(db.DateTime, default=datetime.utcnow)

  # OAuth relationships
  oauth = db.relationship('UserOAuth', backref='user', uselist=False)

  # Many-to-many relationship with roles
  roles = db.relationship('Role', secondary=user_roles, back_populates='users')

  # Relationships for posts, messages, and communities
  posts = db.relationship('Post', backref='author', lazy='dynamic')
  sent_messages = db.relationship('Message',
                                  foreign_keys='Message.sender_id',
                                  backref='sender',
                                  lazy='dynamic')
  received_messages = db.relationship('Message',
                                      foreign_keys='Message.recipient_id',
                                      backref='recipient',
                                      lazy='dynamic')
  comments = db.relationship('Comment', backref='author', lazy='dynamic')
  communities = db.relationship('Community',
                                secondary='user_community',
                                backref=db.backref('members', lazy='dynamic'))

  def __repr__(self):
    return f'<User {self.username}>'

  # Password Hashing
  def set_password(self, password):
    self.password_hash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password_hash, password)

  # Role Checking
  def has_role(self, role_name):
    return any(role.name == role_name for role in self.roles)

  # Assign Role
  def assign_role(self, role):
    if not self.has_role(role.name):
      self.roles.append(role)

  # Remove Role
  def remove_role(self, role):
    if self.has_role(role.name):
      self.roles.remove(role)

  # Super Admin Functions
  def is_super_admin(self):
    return self.has_role('Super Admin')

  def assign_lecturer(self, user):
    if self.is_super_admin():
      lecturer_role = Role.query.filter_by(name='Lecturer').first()
      user.assign_role(lecturer_role)

  def delete_post(self, post):
    if self.is_super_admin():
      db.session.delete(post)
      db.session.commit()
