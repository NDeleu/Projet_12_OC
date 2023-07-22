import os
from configparser import ConfigParser
import secrets
from app.views.general_views.generic_message import display_message


def set_jwt_secret():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    controllers_dir = os.path.dirname(script_dir)
    app_dir = os.path.dirname(controllers_dir)
    root_dir = os.path.dirname(app_dir)
    config_file = os.path.join(root_dir, 'config.ini')
    config = ConfigParser()
    config.read(config_file)

    jwt_secret = config.get('jwt', 'secret_key_jwt')

    if jwt_secret == "default":
        jwt_secret_key = secrets.token_hex(32)
        config.set('jwt', 'secret_key_jwt', jwt_secret_key)

        with open(config_file, 'w') as confchange:
            config.write(confchange)

        display_message("The JWT Secret Key has been configured.")
