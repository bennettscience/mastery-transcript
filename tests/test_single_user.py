import unittest
from app import app, db
from models.user import User


class TestUserEndpoints(unittest.TestCase):
    def setUp(self):
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
        db.create_all()
        self.client = app.test_client()

        u = User(username="Default", email="default@email.com", short_bio='This is a short bio')
        db.session.add(u)
        db.session.commit()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_single_user(self):
        request = self.client.get('/users/1')
        user = request.json
        self.assertEqual(user['username'], 'Default')

