from app import db


class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    short_bio = db.Column(db.String(100))
    long_bio = db.Column(db.String)
    public = db.Column(db.String)

    # def __repr__(self: None) -> str:
    #     # TODO: Connect the profile to the username
    #     return f"This bio for {self.username}"

    # TODO: allow a single profile on the user

    def get_short_bio(self: None) -> str:
        return self.short_bio

    def get_long_bio(self: None) -> str:
        return self.long_bio

    # TODO: Abstract into one function with args
    def set_short_bio(self: None, input: str) -> None:
        # TODO: Validate and sanitize the inputs
        self.short_bio = input

    def set_long_bio(self: None, input: str) -> None:
        # TODO: Validate and sanitize input
        self.long_bio = input

    def update(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
