from app import app, api
from flask import jsonify
from flask_restful import Resource, reqparse, fields, marshal
from models.user import User

user_fields = {
    "id": fields.Integer(), 
    "username": fields.String(),
    "short_bio": fields.String(),
    "long_bio": fields.String()
}


class UsersAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("username", type=str, location="form")
        self.reqparse.add_argument("email", type=str, location="form")
        self.reqparse.add_argument("password", type=str, location="form")

        super(UsersAPI, self).__init__()

    def get(self: None) -> list:
        query = User.query.all()
        users = [user.username for user in query]

        return users, 200


class UserAPI(Resource):
    def get(self, id):
        user = User.query.get(id)
        if user is None:
            return "Not found", 404
        return marshal(user, user_fields)
    
    def post(self, id):
        pass
    
    def put(self, id):
        pass

    def delete(self, id):
        pass



api.add_resource(UsersAPI, "/users", endpoint="users")
api.add_resource(UserAPI, "/users/<id>", endpoint="user/<id>")
