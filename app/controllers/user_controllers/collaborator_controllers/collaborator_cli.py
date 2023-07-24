import click
from .collaborator_controller import create_func, read_func, get_by_id_func, get_by_email_func, update_func, delete_func
from app.views.general_views.generic_message import display_message


@click.group()
def collaborator_form():
    pass


@collaborator_form.command()
@click.pass_context
def create_form(ctx):
    session = ctx.obj
    user = None
    firstname = click.prompt("Firstname", type=click.STRING)
    lastname = click.prompt("Lastname", type=click.STRING)
    email = click.prompt("Email", type=click.STRING)
    display_message("Select: 1 for administrator, 2 for seller, 3 for support")
    role = click.prompt("Role", type=click.INT)
    password = click.prompt("Password", type=click.STRING, hide_input=True)
    create_func(session, user, firstname, lastname, email, role, password)


@collaborator_form.command()
@click.pass_context
def read_form(ctx):
    session = ctx.obj
    user = None
    read_func(session, user)


@collaborator_form.command()
@click.pass_context
def get_by_id_form(ctx):
    session = ctx.obj
    user = None
    collaborator_id = click.prompt("Collaborator_Id", type=click.INT)
    get_by_id_func(session, user, collaborator_id)


@collaborator_form.command()
@click.pass_context
def get_by_email_form(ctx):
    session = ctx.obj
    user = None
    collaborator_email = click.prompt("Email", type=click.STRING)
    get_by_email_func(session, user, collaborator_email)


@collaborator_form.command()
@click.pass_context
def update_form(ctx):
    session = ctx.obj
    user = None
    collaborator_id = click.prompt("Collaborator_Id", type=click.INT)
    firstname = click.prompt("Firstname", type=click.STRING, default=None)
    lastname = click.prompt("Lastname", type=click.STRING, default=None)
    email = click.prompt("Email", type=click.STRING, default=None)
    password = click.prompt("Password", type=click.STRING, hide_input=True, default=None)
    update_func(session, user, collaborator_id, firstname, lastname, email, password)


@collaborator_form.command()
@click.pass_context
def delete_form(ctx):
    session = ctx.obj
    user = None
    collaborator_id = click.prompt("Collaborator_Id", type=click.INT)
    delete_func(session, user, collaborator_id)


@click.group()
def collaborator():
    pass


@collaborator.command()
@click.pass_context
@click.argument('firstname', type=str)
@click.argument('lastname', type=str)
@click.argument('email', type=str)
@click.argument('role', type=int)
@click.argument('password', type=str)
def create(ctx, firstname, lastname, email, role, password):
    session = ctx.obj
    user = None
    create_func(session, user, firstname, lastname, email, role, password)


@collaborator.command()
@click.pass_context
def read(ctx):
    session = ctx.obj
    user = None
    read_func(session, user)


@collaborator.command()
@click.argument('collaborator_id', type=int)
@click.pass_context
def get_by_id(ctx, collaborator_id):
    session = ctx.obj
    user = None
    get_by_id_func(session, user, collaborator_id)


@collaborator.command()
@click.argument('collaborator_email', type=str)
@click.pass_context
def get_by_email(ctx, collaborator_email):
    session = ctx.obj
    user = None
    get_by_email_func(session, user, collaborator_email)


@collaborator.command()
@click.pass_context
@click.argument('collaborator_id', type=int)
@click.option('--firstname', type=str, default=None)
@click.option('--lastname', type=str, default=None)
@click.option('--email', type=str, default=None)
@click.option('--password', type=str, default=None)
def update(ctx, collaborator_id, firstname, lastname, email, password):
    session = ctx.obj
    user = None
    update_func(session, user, collaborator_id, firstname, lastname, email, password)


@collaborator.command()
@click.argument('collaborator_id', type=int)
@click.pass_context
def delete(ctx, collaborator_id):
    session = ctx.obj
    user = None
    delete_func(session, user, collaborator_id)
