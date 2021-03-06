import json

from marshmallow import ValidationError
from marshmallow_sqlalchemy import ModelConversionError, ModelSchema

from app import db


# TODO: This needs some major cleanup
# TODO: reject other inputs (lists, tuples, sets)
def is_json(data: str) -> bool:
    if type(data) is not str:
        data = json.dumps(data)
    try:
        json.loads(data)
    except ValueError:
        return False
    except TypeError:
        return False
    except json.decoder.JSONDecodeError:
        return False
    return True


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
                    sqla_session = db.session
                    load_instance = True

                schema_class_name = "%sSchema" % class_.__name__

                schema_class = type(schema_class_name, (ModelSchema,), {"Meta": Meta})

                setattr(class_, "Schema", schema_class)

    return setup_schema_fn


def update_object(schema, model, data):
    """
    A generic worker to update data within an instantiated class

    :param: schema: Marshmallow schema to use in processing data
    :param: model: Instantiated class to update
    :param: data: JSON object
    """
    # Marshmallow expects a python object, NOT json. Load the input into
    # an object before trying to load the schema.
    if type(data) is str:
        data = json.loads(data)

    try:
        model_session = schema().load(data, instance=model, partial=True)
        model_session.update(**data)
        db.session.commit()
        return schema().dump(model)
    except ValidationError as err:
        return err.messages
