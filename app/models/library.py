"""Library resource model"""
from datetime import datetime
from .. import db

class LibraryItem(db.Model):
    """Model for items in the library, including books, videos, and pictures."""
    __tablename__ = 'library_items'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)  # Title of the item
    description = db.Column(db.String(500), nullable=True)  # Description of the item
    item_type = db.Column(db.String(50), nullable=False)  # Type: book, video, picture
    file_path = db.Column(db.String(255), nullable=False)  # Path to the file
    requires_permission = db.Column(db.Boolean, default=False)  # Whether the item requires permission to download
    permission_password = db.Column(db.String(255), nullable=True)  # Encrypted password for permission
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  # When the item was added

    # Relationship with User
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    owner = db.relationship('User', backref='library_items')

    def save_item(self):
        """Saves the library item to the database."""
        db.session.add(self)
        db.session.commit()

class LibraryRequest(db.Model):
    """Model for requests to download library items that require permission."""
    __tablename__ = 'library_requests'

    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('library_items.id'), nullable=False)
    requester_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    request_timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    item = db.relationship('LibraryItem', backref='requests')
    requester = db.relationship('User', backref='library_requests')

    def save_request(self):
        """Saves the library request to the database."""
        db.session.add(self)
        db.session.commit()
