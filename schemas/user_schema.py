from app import ma
from models.user import User


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        fields = ("username", "email")
        model: User
        load_instance = True
        include_fk = True
        strict = True
