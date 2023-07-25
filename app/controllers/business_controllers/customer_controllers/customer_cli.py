import click
from .customer_controller import create_func, read_func, get_by_id_func, get_by_email_func, update_func, delete_func
from app.views.general_views.generic_message import display_message_info


@click.group()
def customer_form():
    pass


@customer_form.command()
@click.pass_context
def create_form(ctx):
    session = ctx.obj
    user = None
    display_message_info("Firstname in alphabetical value.")
    firstname = click.prompt("Firstname", type=click.STRING)
    display_message_info("Lastname in alphabetical value.")
    lastname = click.prompt("Lastname", type=click.STRING)
    display_message_info("Email in alphabetical value and in form alpha@alpha.alpha.")
    email = click.prompt("Email", type=click.STRING)
    display_message_info("Phone number in numerical value.")
    phone = click.prompt("Phone", type=click.INT)
    display_message_info("Customer's compagny in alphabetical value.")
    company = click.prompt("Company", type=click.STRING)
    create_func(session, user, firstname, lastname, email, phone, company)


@customer_form.command()
@click.pass_context
def read_form(ctx):
    session = ctx.obj
    user = None
    display_message_info("If you are seller, filter awarded customers: True, not this filter: False.")
    mine = click.prompt("Mine", type=click.BOOL, default=False)
    read_func(session, user, mine)


@customer_form.command()
@click.pass_context
def get_by_id_form(ctx):
    session = ctx.obj
    user = None
    display_message_info("Customer ID in numerical value.")
    customer_id = click.prompt("Customer_Id", type=click.INT)
    get_by_id_func(session, user, customer_id)


@customer_form.command()
@click.pass_context
def get_by_email_form(ctx):
    session = ctx.obj
    user = None
    display_message_info("Customer Email in alphabetical value and in form alpha@alpha.alpha.")
    customer_email = click.prompt("Email", type=click.STRING)
    get_by_email_func(session, user, customer_email)


@customer_form.command()
@click.pass_context
def update_form(ctx):
    session = ctx.obj
    user = None
    display_message_info("Customer ID in numerical value.")
    customer_id = click.prompt("Collaborator_id", type=click.INT)
    display_message_info("For change: Firstname in alphabetical value, for keep unchanged: None.")
    firstname = click.prompt("Firstname", type=click.STRING, default=None)
    display_message_info("For change: Lastname in alphabetical value, for keep unchanged: None.")
    lastname = click.prompt("Lastname", type=click.STRING, default=None)
    display_message_info("For change: Email in alphabetical value and in form alpha@alpha.alpha, for keep unchanged: None.")
    email = click.prompt("Email", type=click.STRING, default=None)
    display_message_info("For change: Phone number in numerical value, for keep unchanged: None.")
    phone = click.prompt("Phone", type=click.INT, default=None)
    display_message_info("For change: Customer's compagny in alphabetical value, for keep unchanged: None.")
    company = click.prompt("Company", type=click.STRING, default=None)
    update_func(session, user, customer_id, firstname, lastname, email, phone, company)


@customer_form.command()
@click.pass_context
def delete_form(ctx):
    session = ctx.obj
    user = None
    display_message_info("Customer ID in numerical value")
    customer_id = click.prompt("Customer_Id", type=click.INT)
    delete_func(session, user, customer_id)


@click.group()
def customer():
    pass


@customer.command()
@click.pass_context
@click.argument('firstname', type=str)
@click.argument('lastname', type=str)
@click.argument('email', type=str)
@click.argument('phone', type=int)
@click.argument('company', type=str)
def create(ctx, firstname, lastname, email, phone, company):
    session = ctx.obj
    user = None
    create_func(session, user, firstname, lastname, email, phone, company)


@customer.command()
@click.option('--mine', type=bool, default=False)
@click.pass_context
def read(ctx, mine):
    session = ctx.obj
    user = None
    read_func(session, user, mine)


@customer.command()
@click.argument('customer_id', type=int)
@click.pass_context
def get_by_id(ctx, customer_id):
    session = ctx.obj
    user = None
    get_by_id_func(session, user, customer_id)


@customer.command()
@click.argument('customer_email', type=str)
@click.pass_context
def get_by_email(ctx, customer_email):
    session = ctx.obj
    user = None
    get_by_email_func(session, user, customer_email)


@customer.command()
@click.pass_context
@click.argument('customer_id', type=int)
@click.option('--firstname', type=str, default=None)
@click.option('--lastname', type=str, default=None)
@click.option('--email', type=str, default=None)
@click.option('--phone', type=int, default=None)
@click.option('--company', type=str, default=None)
def update(ctx, customer_id, firstname, lastname, email, phone, company):
    session = ctx.obj
    user = None
    update_func(session, user, customer_id, firstname, lastname, email, phone, company)


@customer.command()
@click.argument('customer_id', type=int)
@click.pass_context
def delete(ctx, customer_id):
    session = ctx.obj
    user = None
    delete_func(session, user, customer_id)
