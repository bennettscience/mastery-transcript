import unittest
from app import app, db
from models.user import User


class TestUserModel(unittest.TestCase):
    def setUp(self):
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
        db.create_all()

        u = User(username="Default", email="default@email.com")
        db.session.add(u)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # Create a new user with a username and password
    def test_create_user(self):
        user = User(username="Test", email="test@email.com")
        user.set_password("password")
        self.assertTrue(user.check_password("password"))
        self.assertFalse(user.check_password("demo"))

    # Change an existing password
    def test_change_password(self):
        user = User.query.filter_by(username="Default").first()
        user.set_password("password")
        self.assertTrue(user.check_password("password"))

    # Set the user profile
    def test_set_user_short_bio(self):
        user = User.query.filter_by(username="Default").first()
        input = "This is my short bio."
        user.set_short_bio(input)
        self.assertEqual(user.short_bio, "This is my short bio.")

    def test_set_user_long_bio(self):
        user = User.query.filter_by(username="Default").first()
        input = "This is my long bio"
        user.set_long_bio(input)
        self.assertEqual(user.long_bio, "This is my long bio")
