from .user import User
from .post import Post
from .comment import Comment
from flask_sqlalchemy import SQLAlchemy
from .community import Community

db = SQLAlchemy()
