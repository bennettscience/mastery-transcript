from app import db


class Artifact(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    type = db.Column(db.String)
    description = db.Column(db.String)

    def get_description(self):
        return self.description

    def update(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
