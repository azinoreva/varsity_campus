from .. import db
from datetime import datetime


# Community Model
class Community(db.Model):
    __tablename__ = 'communities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to posts (community messages)
    messages = db.relationship('CommunityMessage', backref='community', lazy='dynamic')
    
    # Many-to-Many relationship between Users and Communities
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


# Function to add predefined communities to the database comment it out when you first start flask
#def create_communities():
#    for name in community_names:
#        existing_community = Community.query.filter_by(name=name).first()
#        if not existing_community:
#            community = Community(name=name)
#           db.session.add(community)
#   db.session.commit()


# CommunityMessage Model
class CommunityMessage(db.Model):
    __tablename__ = 'community_messages'

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    file_url = db.Column(db.String(255), nullable=True)  # Optional file
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    community_id = db.Column(db.Integer, db.ForeignKey('communities.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    user = db.relationship('User', back_populates='messages')
