from flask import Flask, jsonify
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from config import Config
from marshmallow import ValidationError

__version__ = "0.1"

app = Flask(__name__)
app.config.from_object(Config)
api = Api(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)

from app import app, db
from resources.userapi import UserAPI, UserListAPI, UserProfileAPI, user_ns

api.add_namespace(user_ns)

user_ns.add_resource(UserAPI, "/<int:id>")
user_ns.add_resource(UserListAPI, "/")
user_ns.add_resource(UserProfileAPI, "/<int:id>/profile")


@api.errorhandler(ValidationError)
def handle_validation_error(error):
    return jsonify(error.messages), 400
