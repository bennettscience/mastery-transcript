from flask import abort, request
from flask_restx import Namespace, Resource
from marshmallow import ValidationError

from app import db
from models.user import User
from models.user_profile import UserProfile
from schemas.user_profile_schema import UserProfileSchema
from schemas.user_schema import UserSchema

USER_NOT_FOUND = "User not found"

user_ns = Namespace("users", description="Operations on collections of users.")

user_schema = UserSchema()
many_user_schema = UserSchema(many=True)
user_profile_schema = UserProfileSchema()

user = User()
user_profile = UserProfile()


class UserAPI(Resource):
    def get(self, id):
        user = User.query.get(id)
        if user is None:
            return "Not found", 404
        return user_schema.dump(user), 200

    @user_ns.expect(user)
    def post(self, id):
        pass

    @user_ns.expect(user)
    def put(self, id):
        pass


class UserListAPI(Resource):
    @user_ns.doc("Get all users")
    def get(self: None) -> list:
        return many_user_schema.dump(User.query.all())


class UserProfileAPI(Resource):
    @user_ns.doc("Get a user's profile")
    def get(self: None, id: int) -> UserProfile:
        try:
            user = User.query.get(id)
            if user is None:
                return "Not found", 404
            profile = user.get_profile()
            if profile.public == "false":
                return "This user's profile is private.", 405
            return user_profile_schema.dump(profile), 200
        except Exception as e:
            return e

    @user_ns.expect(user_profile)
    def put(self: None, id: int) -> UserProfile:
        try:
            json_data = request.get_json()
            user_profile = User.query.get(id).profile[0]
            if user_profile is None:
                return "Not found", 404

            if not json_data:
                abort(400)

            profile = UserProfileSchema().load(json_data, instance=user, partial=True)

            profile.update(**json_data)
            db.session.commit()
            return UserProfileSchema().dump(profile), 200
        except ValidationError as err:
            print(request.get_json())
            return err.messages, 422
