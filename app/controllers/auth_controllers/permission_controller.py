import os
from configparser import ConfigParser
from datetime import datetime, timedelta

import jwt

from app.models.class_models.user_models.collaborator_model import Collaborator
from app.views.general_views.generic_message import display_message

script_dir = os.path.dirname(os.path.abspath(__file__))
controllers_dir = os.path.dirname(script_dir)
app_dir = os.path.dirname(controllers_dir)
root_dir = os.path.dirname(app_dir)
config_file = os.path.join(root_dir, 'config.ini')

config = ConfigParser()
config.read(config_file)

SECRET_KEY = config.get('jwt', 'secret_key_jwt')


def generate_token(user_id, role):
    payload = {
        "user_id": user_id,
        "role": role,
        "exp": datetime.utcnow() + timedelta(minutes=10)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


def save_token_to_file(token):
    with open("token.txt", "w") as file:
        file.write(token)


def clear_token_from_file():
    with open("token.txt", "w") as file:
        file.write("")


def get_logged_as_role(session, role_wanted):
    token = get_token_from_file()
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")
            role = payload.get("role")
            if role != role_wanted:
                return None
            else:
                return Collaborator.get_by_id(session, user_id)
        except jwt.ExpiredSignatureError:
            clear_token_from_file()
            return None
    return None


def get_logged_as_user(session):
    token = get_token_from_file()
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")
            return Collaborator.get_by_id(session, user_id)
        except jwt.ExpiredSignatureError:
            clear_token_from_file()
            return None
    return None


def get_token_from_file():
    try:
        with open("token.txt", "r") as file:
            token = file.read().strip()
            return token
    except FileNotFoundError:
        return None


def login_required_admin(func):
    def wrapper(session, *args, **kwargs):
        administrator = get_logged_as_role(session, "administrator")
        if administrator:
            return func(session, *args, **kwargs)
        else:
            display_message("Permission denied. Please log in as an administrator.")
    return wrapper


def login_required_seller(func):
    def wrapper(session, *args, **kwargs):
        administrator = get_logged_as_role(session, "seller")
        if administrator:
            return func(session, *args, **kwargs)
        else:
            display_message("Permission denied. Please log in as an seller.")
    return wrapper


def login_required_support(func):
    def wrapper(session, *args, **kwargs):
        administrator = get_logged_as_role(session, "support")
        if administrator:
            return func(session, *args, **kwargs)
        else:
            display_message("Permission denied. Please log in as an support.")
    return wrapper


def login_required(func):
    def wrapper(session, *args, **kwargs):
        user = get_logged_as_user(session)
        if user:
            return func(session, *args, **kwargs)
        else:
            display_message("Permission denied. Please log in.")
    return wrapper
