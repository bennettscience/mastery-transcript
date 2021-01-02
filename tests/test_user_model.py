import unittest

from app import app, db
from models.user import User
from models.user_profile import UserProfile
from models.user_settings import UserSettings


class TestUserModel(unittest.TestCase):
    def setUp(self):
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
        db.create_all()

        u = User(username="Default", email="default@email.com")
        p = UserProfile(
            user=u, short_bio="This is the short bio.", long_bio="This is the long bio."
        )
        s = UserSettings(
            user=u, canvas_id=12345, token="abcd", expire="999", refresh_token="zyxw"
        )
        db.session.add_all([u, p, s])
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

    def test_user_profile_instance(self):
        user = User.query.filter_by(username="Default").first()
        profile = user.profile[0]
        self.assertIsInstance(profile, UserProfile)

    def test_user_profile_contents(self):
        user = User.query.filter_by(username="Default").first()
        profile = user.profile[0]
        self.assertEqual(profile.short_bio, "This is the short bio.")
        self.assertEqual(profile.long_bio, "This is the long bio.")

    def test_set_short_bio(self):
        user = User.query.filter_by(username="Default").first()
        profile = user.profile[0]
        new_bio = "This is the new short bio"
        profile.set_short_bio(new_bio)
        self.assertEqual(profile.short_bio, new_bio)

    def test_user_settings(self):
        user = User.query.filter_by(username="Default").first()
        settings = user.settings[0]
        self.assertIsNotNone(user.settings)
        self.assertIsInstance(settings, UserSettings)
        self.assertEqual(settings.user_id, 1)
        self.assertEqual(settings.canvas_id, 12345)
