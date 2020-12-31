import unittest
from app import app, db
from models.user import User
from models.user_profile import UserProfile


class TestUserEndpoints(unittest.TestCase):
    def setUp(self):
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
        db.create_all()
        self.client = app.test_client()

        u1 = User(
            username="Default",
            email="default@email.com",
        )
        p1 = UserProfile(
            short_bio="This is the short bio.", public=False, user_id=1
        )

        u2 = User(
            username="Default2",
            email="default2@email.com",
        )
        p2 = UserProfile(
            short_bio="This is the short bio.", public=True, user_id=2
        )
        db.session.add_all([u1, u2, p1, p2])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_single_user(self):
        request = self.client.get("/users/1")
        user = request.json
        self.assertEqual(user["username"], "Default")

    def test_missing_user_profile(self):
        request = self.client.get("/users/999/profile")
        profile = request.json
        print(profile)
        self.assertEqual(request.status_code, 404)
        self.assertEqual(profile, "Not found")

    def test_private_user_profile(self):
        request = self.client.get("/users/1/profile")
        self.assertEqual(request.status_code, 405)

    def test_public_user_profile(self):
        req = self.client.get("/users/2/profile")
        profile = req.json
        self.assertIsInstance(profile, object)
        self.assertIs(profile["public"], True)
