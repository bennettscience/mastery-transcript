import unittest

from app import app, db
from models.user import User
from models.artifact import Artifact


class TestArtifactApi(unittest.TestCase):
    def setUp(self):
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
        db.create_all()
        user = User(username="default", email="default@email.com")

        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_artifact(self):
        a = Artifact(name="item")
        self.assertIsInstance(a, Artifact)

    def test_attach_artifact_to_user(self):
        user = User.query.get(1)
        artifact = Artifact(name="item", user_id=1)
        db.session.add(artifact)
        db.session.commit()
        self.assertEqual(artifact.owner, user)

    def test_attach_many_artifacts(self):
        user = User.query.get(1)
        artifacts = []
        for item in range(0, 3):
            a = Artifact(name=f"Item {item+1}", user_id=1)
            artifacts.append(a)
            db.session.add(a)
        db.session.commit()

        self.assertIsInstance(user.artifacts, list)
        self.assertListEqual(user.artifacts, artifacts)
        self.assertEqual(len(user.artifacts), 3)

    def test_artifact_owner(self):
        user = User.query.get(1)
        a = Artifact(name="Item", user_id=1)
        db.session.add(a)
        db.session.commit()

        self.assertEqual(a.owner, user)
