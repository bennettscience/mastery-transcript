from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), index=True, unique=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    canvas_id = db.Column(db.Integer, unique=True)
    token = db.Column(db.String)
    expire = db.Column(db.Integer)
    refresh_token = db.Column(db.String)
    short_bio = db.Column(db.String(100))
    long_bio = db.Column(db.String)
    public = db.Column(db.Integer)

    # tags relationship
    # outcomes relationship
    def __repr__(self: None) -> str:
        return f"User {self.id}: {self.username}"

    def set_password(self: None, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_short_bio(self: None, input: str) -> None:
        self.short_bio = input

    def set_long_bio(self: None, input: str) -> None:
        self.long_bio = input

    def get_id(self: None) -> int:
        return self.id
    
    def get_short_bio(self: None) -> str:
        return self.short_bio
    
    def get_long_bio(self: None) -> str:
        return self.long_bio
