from flask import Flask, jsonify
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from marshmallow import ValidationError
from marshmallow_sqlalchemy import ModelConversionError, ModelSchema

from config import Config

__version__ = "0.1"

app = Flask(__name__)
app.config.from_object(Config)
api = Api(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)

from app import app, db
from resources.userapi import (
    UserAPI,
    UserListAPI,
    UserProfileAPI,
    UserSettingsAPI,
    user_ns,
)
from resources.artifactapi import ArtifactAPI, ArtifactListAPI, artifact_ns

api.add_namespace(user_ns)
api.add_namespace(artifact_ns)

user_ns.add_resource(UserAPI, "/<int:id>")
user_ns.add_resource(UserListAPI)
user_ns.add_resource(UserProfileAPI, "/<int:id>/profile")
user_ns.add_resource(UserSettingsAPI, "/<int:id>/settings")

artifact_ns.add_resource(ArtifactListAPI, "/<int:user_id>")
artifact_ns.add_resource(ArtifactAPI, "/<int:user_id>/item/<int:id>")


@api.errorhandler(ValidationError)
def handle_validation_error(error):
    return jsonify(error.messages), 400
