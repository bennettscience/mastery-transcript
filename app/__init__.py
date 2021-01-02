from flask import Flask, jsonify
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from marshmallow import ValidationError
from marshmallow_sqlalchemy import ModelConversionError, ModelSchema
from sqlalchemy import event
from sqlalchemy.orm import mapper

from config import Config

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


# Set up custom model schemas automatically
# See https://stackoverflow.com/questions/42891152/how-to-dynamically-generate-marshmallow-schemas-for-sqlalchemy-models


def setup_schema(Base, session):
    # Create a function which incorporates the Base and session information
    def setup_schema_fn():
        for class_ in Base._decl_class_registry.values():
            if hasattr(class_, "__tablename__"):
                if class_.__name__.endswith("Schema"):
                    raise ModelConversionError(
                        "For safety, setup_schema can not be used when a"
                        "Model class ends with 'Schema'"
                    )

                class Meta(object):
                    model = class_
                    sqla_session = session

                schema_class_name = "%sSchema" % class_.__name__

                schema_class = type(schema_class_name, (ModelSchema,), {"Meta": Meta})

                setattr(class_, "Schema", schema_class)

    return setup_schema_fn


event.listen(mapper, "after_configured", setup_schema(db.Model, db.session))


@api.errorhandler(ValidationError)
def handle_validation_error(error):
    return jsonify(error.messages), 400
