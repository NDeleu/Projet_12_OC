import click
from .customer_controller import create_func, read_func, get_by_id_func, get_by_email_func, update_func, delete_func


@click.group()
def customer_form():
    pass


@customer_form.command()
@click.pass_context
def create_form(ctx):
    session = ctx.obj
    user = None
    firstname = click.prompt("Firstname", type=click.STRING)
    lastname = click.prompt("Lastname", type=click.STRING)
    email = click.prompt("Email", type=click.STRING)
    phone = click.prompt("Phone", type=click.INT)
    company = click.prompt("Company", type=click.STRING)
    create_func(session, user, firstname, lastname, email, phone, company)


@customer_form.command()
@click.pass_context
def read_form(ctx):
    session = ctx.obj
    user = None
    read_func(session, user)


@customer_form.command()
@click.pass_context
def get_by_id_form(ctx):
    session = ctx.obj
    collaborator_id = click.prompt("Id", type=click.INT)
    get_by_id_func(session, collaborator_id)


@customer_form.command()
@click.pass_context
def get_by_email_form(ctx):
    session = ctx.obj
    collaborator_email = click.prompt("Email", type=click.STRING)
    get_by_email_func(session, collaborator_email)


@customer_form.command()
@click.pass_context
def update_form(ctx):
    session = ctx.obj
    collaborator_id = click.prompt("Collaborator_id", type=click.INT)
    firstname = click.prompt("Firstname", type=click.STRING, default=None)
    lastname = click.prompt("Lastname", type=click.STRING, default=None)
    email = click.prompt("Email", type=click.STRING, default=None)
    password = click.prompt("Password", type=click.STRING, hide_input=True, default=None)
    update_func(session, collaborator_id, firstname, lastname, email, password)


@customer_form.command()
@click.pass_context
def delete_form(ctx):
    session = ctx.obj
    collaborator_id = click.prompt("Id", type=click.INT)
    delete_func(session, collaborator_id)


@click.group()
def customer():
    pass


@customer.command()
@click.pass_context
@click.argument('firstname', type=str)
@click.argument('lastname', type=str)
@click.argument('email', type=str)
@click.argument('role', type=int)
@click.argument('password', type=str)
def create(ctx, firstname, lastname, email, role, password):
    session = ctx.obj
    create_func(session, firstname, lastname, email, role, password)


@customer.command()
@click.pass_context
def read(ctx):
    session = ctx.obj
    read_func(session)


@customer.command()
@click.argument('collaborator_id', type=int)
@click.pass_context
def get_by_id(ctx, collaborator_id):
    session = ctx.obj
    get_by_id_func(session, collaborator_id)


@customer.command()
@click.argument('collaborator_email', type=str)
@click.pass_context
def get_by_email(ctx, collaborator_email):
    session = ctx.obj
    get_by_email_func(session, collaborator_email)


@customer.command()
@click.pass_context
@click.argument('collaborator_id', type=int)
@click.option('firstname', type=str, default=None)
@click.argument('lastname', type=str, default=None)
@click.argument('email', type=str, default=None)
@click.argument('password', type=str, default=None)
def update(ctx, collaborator_id, firstname, lastname, email, password):
    session = ctx.obj
    update_func(session, collaborator_id, firstname, lastname, email, password)


@customer.command()
@click.argument('collaborator_id', type=int)
@click.pass_context
def delete(ctx, collaborator_id):
    session = ctx.obj
    delete_func(session, collaborator_id)
