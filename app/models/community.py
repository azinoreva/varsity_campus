"""Community Model"""
from .. import db
from datetime import datetime


# Community Model
class Community(db.Model):
    __tablename__ = 'communities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    posts = db.relationship('Post', backref='community', lazy='dynamic')
    members = db.relationship('User',
                              secondary='user_community',
                              backref=db.backref('communities',
                                                 lazy='dynamic'))


# Many-to-Many table between Users and Communities
user_community = db.Table(
    'user_community',
    db.Column('user_id',
              db.Integer,
              db.ForeignKey('users.id'),
              primary_key=True),
    db.Column('community_id',
              db.Integer,
              db.ForeignKey('communities.id'),
              primary_key=True))

# Predefined community names
community_names = [
    "University News", "Lifestyle", "Hangout", "Science and Engineering",
    "Social Science", "The Arts", "Marketplace", "Entertainment", "Politics",
    "General"
]


# Add communities to the database
def create_communities():
    for name in community_names:
        community = Community(name=name)
        db.session.add(community)
    db.session.commit()
