import unittest
from app import create_app, db
from app.models import User

class RouteTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory database for testing
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()  # Create database tables
            # Create a test user
            user = User(username='testuser', email='test@example.com', password='password')
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()  # Drop all tables after tests

    def test_login_route(self):
        response = self.client.post('/login', data={
            'email': 'test@example.com',
            'password': 'password'
        })
        self.assertEqual(response.status_code, 200)  # Check for successful login

    def test_register_route(self):
        response = self.client.post('/register', data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword'
        })
        self.assertEqual(response.status_code, 200)  # Check for successful registration

    def test_communities_route(self):
        response = self.client.get('/communities')
        self.assertEqual(response.status_code, 200)  # Check if communities page loads

if __name__ == '__main__':
    unittest.main()
