from flask_restx import Resource, Namespace
from models.user import User
from schemas.user_schema import UserSchema

USER_NOT_FOUND = "User not found"

user_ns = Namespace("users", description="Operations on collections of users.")

user_schema = UserSchema()
many_user_schema = UserSchema(many=True)

user = User()


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

    def delete(self, id):
        pass


class UserListAPI(Resource):
    @user_ns.doc("Get all users")
    def get(self: None) -> list:
        return many_user_schema.dump(User.query.all())

    @user_ns.expect(user)
    def post(self, id):
        pass
