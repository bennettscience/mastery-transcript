from app import db


class UserSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    canvas_id = db.Column(db.Integer, unique=True)
    token = db.Column(db.String)
    expire = db.Column(db.Integer)
    refresh_token = db.Column(db.String)
