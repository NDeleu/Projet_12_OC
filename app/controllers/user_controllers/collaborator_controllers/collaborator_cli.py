import click
from .collaborator_controller import create_func, read_func, get_by_id_func, get_by_email_func, update_func, delete_func
from app.views.general_views.generic_message import display_message_info, display_message_error


@click.group(help="Collaborator forms command group")
def collaboratorform():
    pass


@collaboratorform.command(help="Create a collaborator with form")
@click.pass_context
def createform(ctx):
    try:
        session = ctx.obj
        display_message_info("Firstname in alphabetical value.")
        firstname = click.prompt("Firstname", type=click.STRING)
        display_message_info("Lastname in alphabetical value.")
        lastname = click.prompt("Lastname", type=click.STRING)
        display_message_info("Email in alphabetical value and in form alpha@alpha.alpha.")
        email = click.prompt("Email", type=click.STRING)
        display_message_info("Role in numerical value, administrator: 1, seller: 2, support: 3.")
        role = click.prompt("Role", type=click.INT)
        display_message_info("Password in form with letters, numbers, and a limited set of special characters (!@#$%^&*()_-).")
        password = click.prompt("Password", type=click.STRING, hide_input=True)
        create_func(session, firstname, lastname, email, role, password)
    except Exception as e:
        display_message_error(str(e))


@collaboratorform.command(help="Get a list of collaborators with form")
@click.pass_context
def readform(ctx):
    try:
        session = ctx.obj
        read_func(session)
    except Exception as e:
        display_message_error(str(e))


@collaboratorform.command(help="Get a collaborator with his ID with form")
@click.pass_context
def getbyidform(ctx):
    try:
        session = ctx.obj
        display_message_info("Collaborator ID in numerical value.")
        collaborator_id = click.prompt("Collaborator_Id", type=click.INT)
        get_by_id_func(session, collaborator_id)
    except Exception as e:
        display_message_error(str(e))


@collaboratorform.command(help="Get a collaborator with his email with form")
@click.pass_context
def getbyemailform(ctx):
    try:
        session = ctx.obj
        display_message_info("Collaborator Email in alphabetical value and in form alpha@alpha.alpha.")
        collaborator_email = click.prompt("Email", type=click.STRING)
        get_by_email_func(session, collaborator_email)
    except Exception as e:
        display_message_error(str(e))


@collaboratorform.command(help="Update a collaborator with form")
@click.pass_context
def updateform(ctx):
    try:
        session = ctx.obj
        display_message_info("Collaborator ID in numerical value.")
        collaborator_id = click.prompt("Collaborator_Id", type=click.INT)
        display_message_info("For change: Firstname in alphabetical value, for keep unchanged: None.")
        firstname = click.prompt("Firstname", type=click.STRING, default=None)
        display_message_info("For change: Lastname in alphabetical value, for keep unchanged: None.")
        lastname = click.prompt("Lastname", type=click.STRING, default=None)
        display_message_info("For change: Email in alphabetical value and in form alpha@alpha.alpha, for keep unchanged: None.")
        email = click.prompt("Email", type=click.STRING, default=None)
        display_message_info("For change: Password in form with letters, numbers, and a limited set of special characters (!@#$%^&*()_-), for keep unchanged: None.")
        password = click.prompt("Password", type=click.STRING, hide_input=True, default=None)
        update_func(session, collaborator_id, firstname, lastname, email, password)
    except Exception as e:
        display_message_error(str(e))


@collaboratorform.command(help="Delete a collaborator with form")
@click.pass_context
def deleteform(ctx):
    try:
        session = ctx.obj
        display_message_info("Collaborator ID in numerical value.")
        collaborator_id = click.prompt("Collaborator_Id", type=click.INT)
        delete_func(session, collaborator_id)
    except Exception as e:
        display_message_error(str(e))


@click.group(help="Collaborator command group")
def collaborator():
    pass


@collaborator.command(help="Create a collaborator with the following arguments:\n\n"
                           "Parameters:\n"
                           "   firstname: Firstname in alphabetical value.\n"
                           "   lastname: Lastname in alphabetical value.\n"
                           "   email: Email in alphabetical value and in form alpha@alpha.alpha.\n"
                           "   role: Role in numerical value, administrator: 1, seller: 2, support: 3.\n"
                           "   password: Password in form with letters, numbers, and a limited set of special characters (!@#$%^&*()_-).")
@click.pass_context
@click.argument('firstname', type=str)
@click.argument('lastname', type=str)
@click.argument('email', type=str)
@click.argument('role', type=int)
@click.argument('password', type=str)
def create(ctx, firstname, lastname, email, role, password):
    try:
        session = ctx.obj
        create_func(session, firstname, lastname, email, role, password)
    except Exception as e:
        display_message_error(str(e))


@collaborator.command(help="Get a list of collaborators")
@click.pass_context
def read(ctx):
    try:
        session = ctx.obj
        read_func(session)
    except Exception as e:
        display_message_error(str(e))


@collaborator.command(help="Get a collaborator with his ID.\n\n"
                           "Parameters:\n"
                            "   collaborator_id: Collaborator ID in numerical value.")
@click.argument('collaborator_id', type=int)
@click.pass_context
def getbyid(ctx, collaborator_id):
    try:
        session = ctx.obj
        get_by_id_func(session, collaborator_id)
    except Exception as e:
        display_message_error(str(e))


@collaborator.command(help="Get a collaborator with his email.\n\n"
                           "Parameters:\n"
                               "   collaborator_email: Collaborator Email in alphabetical value and in form alpha@alpha.alpha.")
@click.argument('collaborator_email', type=str)
@click.pass_context
def getbyemail(ctx, collaborator_email):
    try:
        session = ctx.obj
        get_by_email_func(session, collaborator_email)
    except Exception as e:
        display_message_error(str(e))


@collaborator.command(help="Update a collaborator with the following options:\n\n"
                           "Parameters:\n"
                           "   collaborator_id: Collaborator ID in numerical value.\n"
                           "Options:\n"
                           "   --firstname: For change: Firstname in alphabetical value, for keep unchanged: None.\n"
                           "   --lastname: For change: Lastname in alphabetical value, for keep unchanged: None.\n"
                           "   --email: For change: Email in alphabetical value and in form alpha@alpha.alpha, for keep unchanged: None.\n"
                           "   --password: For change: Password in form with letters, numbers, and a limited set of special characters (!@#$%^&*()_-), for keep unchanged: None.")
@click.pass_context
@click.argument('collaborator_id', type=int)
@click.option('--firstname', type=str, default=None, help="For change: Firstname in alphabetical value, for keep unchanged: None.")
@click.option('--lastname', type=str, default=None, help="For change: Lastname in alphabetical value, for keep unchanged: None.")
@click.option('--email', type=str, default=None, help="For change: Email in alphabetical value and in form alpha@alpha.alpha, for keep unchanged: None.")
@click.option('--password', type=str, default=None, help="For change: Password in form with letters, numbers, and a limited set of special characters (!@#$%^&*()_-), for keep unchanged: None.")
def update(ctx, collaborator_id, firstname, lastname, email, password):
    try:
        session = ctx.obj
        update_func(session, collaborator_id, firstname, lastname, email, password)
    except Exception as e:
        display_message_error(str(e))


@collaborator.command(help="Delete a collaborator with the following argument:\n\n"
                           "Parameters:\n"
                           "   collaborator_id: Collaborator ID in numerical value.")
@click.argument('collaborator_id', type=int)
@click.pass_context
def delete(ctx, collaborator_id):
    try:
        session = ctx.obj
        delete_func(session, collaborator_id)
    except Exception as e:
        display_message_error(str(e))
