import unittest

from app import app, db
from models.artifact import Artifact
from models.user import User


class TestArtifactEndpoints(unittest.TestCase):
    def setUp(self):
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
        db.create_all()
        self.client = app.test_client()

        u1 = User(username="Default", email="default@email.com")
        u2 = User(username="Default2", email="default2@email.com")

        for user in range(0, 2):
            for item in range(0, 3):
                item = Artifact(name=f"Item {item+1}", user_id=user + 1)
                db.session.add(item)
                db.session.commit()

        db.session.add_all([u1, u2])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_artifacts_for_user(self):
        req = self.client.get("/artifacts/1")
        artifacts = req.get_json()
        self.assertIsInstance(artifacts, object)
        self.assertEqual(artifacts["length"], 3)

    def test_get_single_item_for_user(self):
        req = self.client.get("/artifacts/1/item/1")
        item = req.get_json()
        self.assertIsInstance(item, object)
        self.assertEqual(item["name"], "Item 1")
