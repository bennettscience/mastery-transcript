import json

from flask import abort, request
from flask_restx import Namespace, Resource
from marshmallow import ValidationError
from sqlalchemy import event
from sqlalchemy.orm import mapper

from app import db
from app.utils import is_json, setup_schema, update_object
from models.user import User
from models.user_profile import UserProfile
from models.user_settings import UserSettings

event.listen(mapper, "after_configured", setup_schema(db.Model, db.session))

user_ns = Namespace("users", description="Operations on collections of users.")

user = User()
user_profile = UserProfile()
user_settings = UserSettings()

user_schema = User.Schema()
many_user_schema = User.Schema()
user_profile_schema = UserProfile.Schema()
user_settings_schema = UserSettings.Schema()


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

    def put(self: None, id: int) -> UserProfile:
        try:
            json_data = request.get_json()

            user_profile = User.query.get(id).profile[0]
            if user_profile is None:
                return "Not found", 404

            if not is_json(json_data):
                return {"message": "Bad request.", "data": json_data}, 400

            result = update_object(UserProfile.Schema, user_profile, json_data)
            return result

        except ValidationError as err:
            print(request.get_json())
            return err.messages, 422


class UserSettingsAPI(Resource):
    @user_ns.doc("Settings for a user")
    def get(self: None, id: int) -> str:
        user = User.query.get(id)
        if user is None:
            return "Not found", 404
        return user_settings_schema.dump(user.settings), 200

    def put(self: None, id: int) -> str:
        json_data = request.get_json()
        user_settings = User.query.get(id).settings[0]
        if user is None:
            return "Not found", 404

        if not is_json(json_data):
            return {"message": "Bad request.", "data": json_data}, 400

        return update_object(UserSettings.Schema, user_settings, json_data)
