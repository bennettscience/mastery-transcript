from app import ma
from models.user_profile import UserProfile


class UserProfileSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        fields = ("short_bio", "long_bio", "public")
        model = UserProfile
        load_instance = True
