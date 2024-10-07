from .user import User
from .post import Post
from .comment import Comment
from flask_sqlalchemy import SQLAlchemy
from .community import Community
from .lecture import Lecture
from .course import Course

db = SQLAlchemy()
