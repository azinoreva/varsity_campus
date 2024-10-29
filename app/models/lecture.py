"""Lecture Model"""

from datetime import datetime
from .. import db


# Lecture Model
class Lecture(db.Model):
  __tablename__ = 'lectures'

  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(100), nullable=False)  # Lecture title
  description = db.Column(db.String(255), nullable=True)  # Lecture description
  created_at = db.Column(db.DateTime, default=datetime.utcnow)
  notes = db.Column(db.String(5000), nullable=True)
  start_date = db.Column(db.DateTime, nullable=True)  # Optional start date
  end_date = db.Column(db.DateTime, nullable=True) #optional end date

  # Relationships
  lecturer_id = db.Column(db.Integer,
                          db.ForeignKey('users.id'),
                          nullable=False)  # Only lecturers can create
  students = db.relationship('User',
                             secondary='lecture_students',
                             backref='lectures')  # Students in the lecture
  videos = db.relationship('LectureVideo', backref='lecture',
                           lazy=True)  # Videos related to lecture
  documents = db.relationship('LectureDocument', backref='lecture',
                              lazy=True)  # Documents related to lecture
  assignments = db.relationship('Assignment', backref='lecture',
                                lazy=True)  # Assignments
  notifications = db.relationship('Notification', backref='lecture',
                                  lazy=True)  # Notifications


# Many-to-Many table for students and lectures
lecture_students = db.Table(
    'lecture_students',
    db.Column('student_id',
              db.Integer,
              db.ForeignKey('users.id'),
              primary_key=True),
    db.Column('lecture_id',
              db.Integer,
              db.ForeignKey('lectures.id'),
              primary_key=True))


# Lecture Video Model
class LectureVideo(db.Model):
  __tablename__ = 'lecture_videos'

  id = db.Column(db.Integer, primary_key=True)
  video_url = db.Column(db.String(255), nullable=False)
  lecture_id = db.Column(db.Integer,
                         db.ForeignKey('lectures.id'),
                         nullable=False)


# Lecture Document Model
class LectureDocument(db.Model):
  __tablename__ = 'lecture_documents'

  id = db.Column(db.Integer, primary_key=True)
  document_path = db.Column(db.String(255), nullable=False)
  lecture_id = db.Column(db.Integer,
                         db.ForeignKey('lectures.id'),
                         nullable=False)


# Notification Model
class Notification(db.Model):
  __tablename__ = 'notifications'

  id = db.Column(db.Integer, primary_key=True)
  message = db.Column(db.String(255), nullable=False)
  timestamp = db.Column(db.DateTime, default=datetime.utcnow)
  lecture_id = db.Column(db.Integer,
                         db.ForeignKey('lectures.id'),
                         nullable=False)


# Assignment Model
class Assignment(db.Model):
  __tablename__ = 'assignments'

  id = db.Column(db.Integer, primary_key=True)
  description = db.Column(db.String(255), nullable=True)  # Assignment details
  content = db.Column(db.String(5000), nullable=True)
  due_date = db.Column(db.DateTime, nullable=False)
  lecture_id = db.Column(db.Integer,
                         db.ForeignKey('lectures.id'),
                         nullable=False)
  student_id = db.Column(db.Integer,
                         db.ForeignKey('users.id'),
                         nullable=False)
  lecturer_id = db.Column(db.Integer,
                         db.ForeignKey('users.id'),
                         nullable=False)
