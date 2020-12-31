from app import app, db
from models.artifact import Artifact
from models.user import User
from models.user_profile import UserProfile
from models.user_settings import UserSettings


@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "app": app,
        "Artifact": Artifact,
        "User": User,
        "UserProfile": UserProfile,
        "UserSettings": UserSettings
    }
