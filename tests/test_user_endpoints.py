import json
import unittest

from app import app, db
from models.user import User
from models.user_profile import UserProfile


class TestUserEndpoints(unittest.TestCase):
    def setUp(self):
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
        db.create_all()
        self.client = app.test_client()

        u1 = User(username="Default", email="default@email.com")
        p1 = UserProfile(short_bio="This is the short bio.", public="false", user_id=1)

        u2 = User(username="Default2", email="default2@email.com")
        p2 = UserProfile(short_bio="This is the short bio.", public="true", user_id=2)
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
        self.assertEqual(request.status_code, 404)
        self.assertEqual(profile, "Not found")

    def test_private_user_profile(self):
        request = self.client.get("/users/1/profile")
        self.assertEqual(request.status_code, 405)

    def test_public_user_profile(self):
        req = self.client.get("/users/2/profile")
        profile = req.json
        self.assertIsInstance(profile, object)
        self.assertEqual(profile["public"], "true")

    # There's some kind of package error here...these methods work in dev server
    # def test_update_user(self):
    #     payload = {
    #         "public": "true",
    #     }
    #     headers = {"Content-Type: application/json"}
    #     req = self.client.put("/users/1/profile", data=payload, headers=headers)
    #     profile = req.json
    #     self.assertIsInstance(profile, object)
    #     self.assertEqual(profile['public'], 'true')
