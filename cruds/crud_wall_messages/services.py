from flask import jsonify, Blueprint, request
from . import models
from backend import db


wall_messages = Blueprint("wall_messages", __name__)
