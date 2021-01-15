import unittest

from app import app, db
from models.user import User
from models.user_profile import UserProfile
from models.user_settings import UserSettings


class TestUserEndpoints(unittest.TestCase):
    def setUp(self):
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
        db.create_all()
        self.client = app.test_client()

        u1 = User(username="Default", email="default@email.com")
        p1 = UserProfile(short_bio="This is the short bio.", public="false", user_id=1)

        u2 = User(username="Default2", email="default2@email.com")
        p2 = UserProfile(short_bio="This is the short bio.", public="true", user_id=2)

        s1 = UserSettings(user=u1, canvas_id=12345)
        s2 = UserSettings(user=u2, canvas_id=98765)
        db.session.add_all([u1, u2, p1, p2, s1, s2])
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

    def test_bad_user_update_data(self):
        payload = "this should fail"
        headers = {"Content-Type": "application/json"}
        req = self.client.put("/users/1/profile", json=payload, headers=headers)
        self.assertEqual(req.status_code, 400)

    def test_update_user(self):
        payload = {"public": "true"}
        headers = {"Content-Type": "application/json"}
        req = self.client.put("/users/1/profile", json=payload, headers=headers)
        profile = req.json
        self.assertEqual(req.status_code, 200)
        self.assertIsInstance(profile, object)

    def test_string_update_user(self):
        payload = '{"public": "true"}'
        headers = headers = {"Content-Type": "application/json"}
        req = self.client.put("/users/1/profile", json=payload, headers=headers)
        profile = req.json
        self.assertEqual(req.status_code, 200)
        self.assertIsInstance(profile, object)

    def test_missing_user_settings(self):
        req = self.client.get("/users/99/settings")
        self.assertEqual(req.status_code, 404)

    def test_user_settings(self):
        req = self.client.get("/users/1/settings")
        settings = req.json
        self.assertEqual(req.status_code, 200)
        self.assertIsInstance(settings, object)

    # def test_update_user_settings(self):
    #     headers = {"Content-Type": "application/json"}
    #     payload = {
    #         ""
    #     }
    #     req = self.client.get("/users/1/settings")
