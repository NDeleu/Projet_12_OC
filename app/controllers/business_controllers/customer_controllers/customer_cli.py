import click
from .customer_controller import create_func, read_func, get_by_id_func, get_by_email_func, update_func, delete_func
from app.views.general_views.generic_message import display_message_info


@click.group(help="Customer forms command group")
def customer_form():
    pass


@customer_form.command(help="Create a customer with form")
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


@customer_form.command(help="Get a list of customers with form")
@click.pass_context
def read_form(ctx):
    session = ctx.obj
    user = None
    display_message_info("If you are seller, filter awarded customers: True, not this filter: False.")
    mine = click.prompt("Mine", type=click.BOOL, default=False)
    read_func(session, user, mine)


@customer_form.command(help="Get a customer with his ID with form")
@click.pass_context
def get_by_id_form(ctx):
    session = ctx.obj
    user = None
    display_message_info("Customer ID in numerical value.")
    customer_id = click.prompt("Customer_Id", type=click.INT)
    get_by_id_func(session, user, customer_id)


@customer_form.command(help="Get a customer with his email with form")
@click.pass_context
def get_by_email_form(ctx):
    session = ctx.obj
    user = None
    display_message_info("Customer Email in alphabetical value and in form alpha@alpha.alpha.")
    customer_email = click.prompt("Email", type=click.STRING)
    get_by_email_func(session, user, customer_email)


@customer_form.command(help="Update a customer with form")
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


@customer_form.command(help="Delete a customer with form")
@click.pass_context
def delete_form(ctx):
    session = ctx.obj
    user = None
    display_message_info("Customer ID in numerical value")
    customer_id = click.prompt("Customer_Id", type=click.INT)
    delete_func(session, user, customer_id)


@click.group(help="Customer command group")
def customer():
    pass


@customer.command(help="Create a customer")
@click.pass_context
@click.argument('firstname', type=str, help="Firstname in alphabetical value.")
@click.argument('lastname', type=str, help="Lastname in alphabetical value.")
@click.argument('email', type=str, help="Email in alphabetical value and in form alpha@alpha.alpha.")
@click.argument('phone', type=int, help="Phone number in numerical value.")
@click.argument('company', type=str, help="Customer's compagny in alphabetical value.")
def create(ctx, firstname, lastname, email, phone, company):
    session = ctx.obj
    user = None
    create_func(session, user, firstname, lastname, email, phone, company)


@customer.command(help="Get a list of customers")
@click.option('--mine', type=bool, default=False, help="If you are seller, filter awarded customers: True, not this filter: False.")
@click.pass_context
def read(ctx, mine):
    session = ctx.obj
    user = None
    read_func(session, user, mine)


@customer.command(help="Get a customer with his ID")
@click.argument('customer_id', type=int, help="Customer ID in numerical value.")
@click.pass_context
def get_by_id(ctx, customer_id):
    session = ctx.obj
    user = None
    get_by_id_func(session, user, customer_id)


@customer.command(help="Get a customer with his email")
@click.argument('customer_email', type=str, help="Customer Email in alphabetical value and in form alpha@alpha.alpha.")
@click.pass_context
def get_by_email(ctx, customer_email):
    session = ctx.obj
    user = None
    get_by_email_func(session, user, customer_email)


@customer.command(help="Update a customer")
@click.pass_context
@click.argument('customer_id', type=int, help="Customer ID in numerical value.")
@click.option('--firstname', type=str, default=None, help="For change: Firstname in alphabetical value, for keep unchanged: None.")
@click.option('--lastname', type=str, default=None, help="For change: Lastname in alphabetical value, for keep unchanged: None.")
@click.option('--email', type=str, default=None, help="For change: Email in alphabetical value and in form alpha@alpha.alpha, for keep unchanged: None.")
@click.option('--phone', type=int, default=None, help="For change: Phone number in numerical value, for keep unchanged: None.")
@click.option('--company', type=str, default=None, help="For change: Customer's compagny in alphabetical value, for keep unchanged: None.")
def update(ctx, customer_id, firstname, lastname, email, phone, company):
    session = ctx.obj
    user = None
    update_func(session, user, customer_id, firstname, lastname, email, phone, company)


@customer.command(help="Delete a customer")
@click.argument('customer_id', type=int, help="Customer ID in numerical value.")
@click.pass_context
def delete(ctx, customer_id):
    session = ctx.obj
    user = None
    delete_func(session, user, customer_id)
