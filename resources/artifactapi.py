import json
from flask import request
from flask_restx import Namespace, Resource
from marshmallow import ValidationError
from sqlalchemy import event
from sqlalchemy.orm import mapper

from app import db
from app.utils import is_json, setup_schema, update_object
from models.artifact import Artifact
from models.user import User


event.listen(mapper, "after_configured", setup_schema(db.Model, db.session))

artifact_ns = Namespace(
    "artifacts", description="Ops on artifacts attached as evidence."
)

artifact = Artifact()
user = User()

artifact_schema = Artifact.Schema()
user_schema = User.Schema()


class ArtifactListAPI(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        artifacts = [artifact_schema.dump(item) for item in user.artifacts]
        return {"length": len(artifacts), "items": artifacts}, 200


class ArtifactAPI(Resource):
    def get(self, user_id, id):
        item = Artifact.query.filter_by(user_id=user_id, id=id).first()
        return item.Schema().dump(item), 200

    def put(self, user_id, id):
        json_data = request.get_json()
        artifact = Artifact.query.filter_by(user_id=user_id, id=id).first()

        if not is_json(json_data):
            return {"message": "Bad request", "data": json_data}, 400

        result = update_object(Artifact.Schema, artifact, json_data)
        return result
