""" Message model"""
from datetime import datetime
from flask_login import UserMixin
from .. import db
from cryptography.fernet import Fernet


class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer,
                          db.ForeignKey('users.id'),
                          nullable=False)
    receiver_id = db.Column(db.Integer,
                            db.ForeignKey('users.id'),
                            nullable=True)  # For direct messages
    channel_id = db.Column(db.Integer,
                           db.ForeignKey('channels.id'),
                           nullable=True)  # For group messages (channels)
    content = db.Column(db.Text, nullable=False)
    encrypted_content = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    read = db.Column(db.Boolean, default=False)
    reactions = db.relationship('Reaction', backref='message',
                                lazy=True)  # Users can react to messages

    def __init__(self,
                 sender_id,
                 receiver_id=None,
                 channel_id=None,
                 content=""):
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.channel_id = channel_id
        self.content = content
        self.encrypted_content = self.encrypt_message(content)

    def encrypt_message(self, content):
        """Encrypt the message content."""
        key = Fernet.generate_key()  # Should be consistent per session
        f = Fernet(key)
        return f.encrypt(content.encode('utf-8')).decode('utf-8')

    def decrypt_message(self, encrypted_content):
        """Decrypt the message content."""
        key = Fernet.generate_key()  # Use the same key as used for encryption
        f = Fernet(key)
        return f.decrypt(encrypted_content.encode('utf-8')).decode('utf-8')


class Reaction(db.Model):
    __tablename__ = 'reactions'

    id = db.Column(db.Integer, primary_key=True)
    message_id = db.Column(db.Integer,
                           db.ForeignKey('messages.id'),
                           nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    emoji = db.Column(db.String(10), nullable=False)  # Emoji reaction


# Channel Model for Group Messaging
class Channel(db.Model):
    __tablename__ = 'channels'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    messages = db.relationship('Message', backref='channel', lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer,
                           db.ForeignKey('users.id'),
                           nullable=False)  # Channel creator

    def __init__(self, name, description, created_by):
        self.name = name
        self.description = description
        self.created_by = created_by
