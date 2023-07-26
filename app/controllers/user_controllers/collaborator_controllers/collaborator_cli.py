import click
from .collaborator_controller import create_func, read_func, get_by_id_func, get_by_email_func, update_func, delete_func
from app.views.general_views.generic_message import display_message_info, display_message_error


@click.group(help="Collaborator forms command group")
def collaborator_form():
    pass


@collaborator_form.command(help="Create a collaborator with form")
@click.pass_context
def create_form(ctx):
    try:
        session = ctx.obj
        user = None
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
        create_func(session, user, firstname, lastname, email, role, password)
    except Exception as e:
        display_message_error(str(e))


@collaborator_form.command(help="Get a list of collaborators with form")
@click.pass_context
def read_form(ctx):
    try:
        session = ctx.obj
        user = None
        read_func(session, user)
    except Exception as e:
        display_message_error(str(e))


@collaborator_form.command(help="Get a collaborator with his ID with form")
@click.pass_context
def get_by_id_form(ctx):
    try:
        session = ctx.obj
        user = None
        display_message_info("Collaborator ID in numerical value.")
        collaborator_id = click.prompt("Collaborator_Id", type=click.INT)
        get_by_id_func(session, user, collaborator_id)
    except Exception as e:
        display_message_error(str(e))


@collaborator_form.command(help="Get a collaborator with his email with form")
@click.pass_context
def get_by_email_form(ctx):
    try:
        session = ctx.obj
        user = None
        display_message_info("Collaborator Email in alphabetical value and in form alpha@alpha.alpha.")
        collaborator_email = click.prompt("Email", type=click.STRING)
        get_by_email_func(session, user, collaborator_email)
    except Exception as e:
        display_message_error(str(e))


@collaborator_form.command(help="Update a collaborator with form")
@click.pass_context
def update_form(ctx):
    try:
        session = ctx.obj
        user = None
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
        update_func(session, user, collaborator_id, firstname, lastname, email, password)
    except Exception as e:
        display_message_error(str(e))


@collaborator_form.command(help="Delete a collaborator with form")
@click.pass_context
def delete_form(ctx):
    try:
        session = ctx.obj
        user = None
        display_message_info("Collaborator ID in numerical value.")
        collaborator_id = click.prompt("Collaborator_Id", type=click.INT)
        delete_func(session, user, collaborator_id)
    except Exception as e:
        display_message_error(str(e))


@click.group(help="Collaborator command group")
def collaborator():
    pass


@collaborator.command(help="Create a collaborator")
@click.pass_context
@click.argument('firstname', type=str, help="Firstname in alphabetical value.")
@click.argument('lastname', type=str, help="Lastname in alphabetical value.")
@click.argument('email', type=str, help="Email in alphabetical value and in form alpha@alpha.alpha.")
@click.argument('role', type=int, help="Role in numerical value, administrator: 1, seller: 2, support: 3.")
@click.argument('password', type=str, help="Password in form with letters, numbers, and a limited set of special characters (!@#$%^&*()_-).")
def create(ctx, firstname, lastname, email, role, password):
    try:
        session = ctx.obj
        user = None
        create_func(session, user, firstname, lastname, email, role, password)
    except Exception as e:
        display_message_error(str(e))


@collaborator.command(help="Get a list of collaborators")
@click.pass_context
def read(ctx):
    try:
        session = ctx.obj
        user = None
        read_func(session, user)
    except Exception as e:
        display_message_error(str(e))


@collaborator.command(help="Get a collaborator with his ID")
@click.argument('collaborator_id', type=int, help="Collaborator ID in numerical value.")
@click.pass_context
def get_by_id(ctx, collaborator_id):
    try:
        session = ctx.obj
        user = None
        get_by_id_func(session, user, collaborator_id)
    except Exception as e:
        display_message_error(str(e))


@collaborator.command(help="Get a collaborator with his email")
@click.argument('collaborator_email', type=str, help="Collaborator Email in alphabetical value and in form alpha@alpha.alpha.")
@click.pass_context
def get_by_email(ctx, collaborator_email):
    try:
        session = ctx.obj
        user = None
        get_by_email_func(session, user, collaborator_email)
    except Exception as e:
        display_message_error(str(e))


@collaborator.command(help="Update a collaborator")
@click.pass_context
@click.argument('collaborator_id', type=int, help="Collaborator ID in numerical value.")
@click.option('--firstname', type=str, default=None, help="For change: Firstname in alphabetical value, for keep unchanged: None.")
@click.option('--lastname', type=str, default=None, help="For change: Lastname in alphabetical value, for keep unchanged: None.")
@click.option('--email', type=str, default=None, help="For change: Email in alphabetical value and in form alpha@alpha.alpha, for keep unchanged: None.")
@click.option('--password', type=str, default=None, help="For change: Password in form with letters, numbers, and a limited set of special characters (!@#$%^&*()_-), for keep unchanged: None.")
def update(ctx, collaborator_id, firstname, lastname, email, password):
    try:
        session = ctx.obj
        user = None
        update_func(session, user, collaborator_id, firstname, lastname, email, password)
    except Exception as e:
        display_message_error(str(e))


@collaborator.command(help="Delete a collaborator")
@click.argument('collaborator_id', type=int, help="Collaborator ID in numerical value.")
@click.pass_context
def delete(ctx, collaborator_id):
    try:
        session = ctx.obj
        user = None
        delete_func(session, user, collaborator_id)
    except Exception as e:
        display_message_error(str(e))
