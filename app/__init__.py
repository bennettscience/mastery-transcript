import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, session
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_debugtoolbar import DebugToolbarExtension
from config import Config

__version__ = '0.1'

app = Flask(__name__)
app.config.from_object(Config)
api = Api(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import users
from models.user import User
