from werkzeug.security import check_password_hash, generate_password_hash

from app import db
from models.artifact import Artifact
from models.user_profile import UserProfile
from models.user_settings import UserSettings


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), index=True, unique=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    settings = db.relationship(UserSettings, backref="user")
    profile = db.relationship(UserProfile, backref="user")
    artifacts = db.relationship(Artifact, backref="owner")

    # tags relationship
    # outcomes relationship
    def __repr__(self: None) -> str:
        return f"User {self.id}: {self.username}"

    def set_password(self: None, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self: None) -> int:
        return self.id

    def get_profile(self: None) -> UserProfile:
        return self.profile[0]
