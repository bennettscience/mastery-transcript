from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), index=True, unique=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    # tags relationship
    # outcomes relationship
    def __repr__(self: None) -> str:
        return f"User: {self.username}"

    def __init__(self: None, id: int, username: str, email: str) -> None:
        self.id = id
        self.username = username
        self.email = email
