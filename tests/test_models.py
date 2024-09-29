import unittest
from app import create_app, db
from app.models import User, Community, Lecture, Course

class ModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory database for testing
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()  # Create database tables

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()  # Drop all tables after tests

    def test_user_creation(self):
        user = User(username='testuser', email='test@example.com', password='password')
        with self.app.app_context():
            db.session.add(user)
            db.session.commit()
            self.assertIsNotNone(user.id)

    def test_community_creation(self):
        community = Community(name='Test Community', description='A community for testing.')
        with self.app.app_context():
            db.session.add(community)
            db.session.commit()
            self.assertIsNotNone(community.id)

    def test_lecture_creation(self):
        lecture = Lecture(title='Test Lecture', description='A lecture for testing.')
        with self.app.app_context():
            db.session.add(lecture)
            db.session.commit()
            self.assertIsNotNone(lecture.id)

    def test_course_creation(self):
        course = Course(name='Test Course', description='A course for testing.')
        with self.app.app_context():
            db.session.add(course)
            db.session.commit()
            self.assertIsNotNone(course.id)

if __name__ == '__main__':
    unittest.main()
