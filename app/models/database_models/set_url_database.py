import os
import re
from configparser import ConfigParser
from app.views.general_views.generic_message import display_message


def set_url_config():
    if choice_change_url():
        set_sql_config_ini()
        return True
    else:
        return False


def choice_change_url():
    while True:
        display_message("Do you want change your Database configuration now ?")
        try:
            change_select_choice = int(input(display_message("Select 1 for yes or 2 for no: ")))
            if change_select_choice == 1:
                selected_choice = True
                break
            elif change_select_choice == 2:
                selected_choice = False
                break
            else:
                display_message("Invalid choice. Please try again.")
        except ValueError:
            display_message("Invalid input. Please enter a valid choice.")
    return selected_choice


def form_url_config():
    while True:
        username_choice = str(input(
            display_message("Enter your database administrator username: ")))

        if re.match("^[a-zA-Z0-9]+$", username_choice):
            break
        else:
            display_message(
                "Invalid input. Please enter a valid username without special characters or spaces.")

    while True:
        password_choice = str(input(display_message("Enter your database password: ")))
        if password_choice.strip():
            break
        else:
            display_message(
                "Invalid input. Please enter a non-empty password.")

    while True:
        database_name_choice = str(
            input(display_message("Enter your database name: ")))

        # Vérification avec une expression régulière pour restreindre à alphanumérique
        if re.match("^[a-zA-Z0-9]+$", database_name_choice):
            break
        else:
            display_message(
                "Invalid input. Please enter a valid database name without special characters or spaces.")

    sett = {
        'username': username_choice,
        'password': password_choice,
        'database_name': database_name_choice,
    }

    return sett


def set_sql_config_ini():

    sql_init_config_set = form_url_config()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    controllers_dir = os.path.dirname(script_dir)
    app_dir = os.path.dirname(controllers_dir)
    root_dir = os.path.dirname(app_dir)
    config_file = os.path.join(root_dir, 'config.ini')

    config = ConfigParser()
    config.read(config_file)

    config.set('sql', 'username', sql_init_config_set['username'])
    config.set('sql', 'password', sql_init_config_set['password'])
    config.set('sql', 'database_name', sql_init_config_set['database_name'])

    with open(config_file, 'w') as confchange:
        config.write(confchange)
