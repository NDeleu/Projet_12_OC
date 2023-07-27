import click
from .customer_controller import create_func, read_func, get_by_id_func, get_by_email_func, update_func, delete_func
from app.views.general_views.generic_message import display_message_info, display_message_error


@click.group(help="Customer forms command group")
def customerform():
    pass


@customerform.command(help="Create a customer with form")
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
        display_message_info("Phone number in numerical value.")
        phone = click.prompt("Phone", type=click.STRING)
        display_message_info("Customer's compagny in alphabetical value.")
        company = click.prompt("Company", type=click.STRING)
        create_func(session, firstname, lastname, email, phone, company)
    except Exception as e:
        display_message_error(str(e))


@customerform.command(help="Get a list of customers with form")
@click.pass_context
def readform(ctx):
    try:
        session = ctx.obj
        display_message_info("If you are seller, filter awarded customers: True, not this filter: False.")
        mine = click.prompt("Mine", type=click.BOOL, default=False)
        read_func(session, mine)
    except Exception as e:
        display_message_error(str(e))


@customerform.command(help="Get a customer with his ID with form")
@click.pass_context
def getbyidform(ctx):
    try:
        session = ctx.obj
        display_message_info("Customer ID in numerical value.")
        customer_id = click.prompt("Customer_Id", type=click.INT)
        get_by_id_func(session, customer_id)
    except Exception as e:
        display_message_error(str(e))


@customerform.command(help="Get a customer with his email with form")
@click.pass_context
def getbyemailform(ctx):
    try:
        session = ctx.obj
        display_message_info("Customer Email in alphabetical value and in form alpha@alpha.alpha.")
        customer_email = click.prompt("Email", type=click.STRING)
        get_by_email_func(session, customer_email)
    except Exception as e:
        display_message_error(str(e))


@customerform.command(help="Update a customer with form")
@click.pass_context
def updateform(ctx):
    try:
        session = ctx.obj
        display_message_info("Customer ID in numerical value.")
        customer_id = click.prompt("Collaborator_id", type=click.INT)
        display_message_info("For change: Firstname in alphabetical value, for keep unchanged: None.")
        firstname = click.prompt("Firstname", type=click.STRING, default=None)
        display_message_info("For change: Lastname in alphabetical value, for keep unchanged: None.")
        lastname = click.prompt("Lastname", type=click.STRING, default=None)
        display_message_info("For change: Email in alphabetical value and in form alpha@alpha.alpha, for keep unchanged: None.")
        email = click.prompt("Email", type=click.STRING, default=None)
        display_message_info("For change: Phone number in numerical value, for keep unchanged: None.")
        phone = click.prompt("Phone", type=click.STRING, default=None)
        display_message_info("For change: Customer's compagny in alphabetical value, for keep unchanged: None.")
        company = click.prompt("Company", type=click.STRING, default=None)
        update_func(session, customer_id, firstname, lastname, email, phone, company)
    except Exception as e:
        display_message_error(str(e))


@customerform.command(help="Delete a customer with form")
@click.pass_context
def deleteform(ctx):
    try:
        session = ctx.obj
        display_message_info("Customer ID in numerical value")
        customer_id = click.prompt("Customer_Id", type=click.INT)
        delete_func(session, customer_id)
    except Exception as e:
        display_message_error(str(e))


@click.group(help="Customer command group")
def customer():
    pass


@customer.command(help="Create a customer\n\n"
                          "Parameters:\n"
                          "   firstname (str): Firstname in alphabetical value.\n"
                          "   lastname (str): Lastname in alphabetical value.\n"
                          "   email (str): Email in alphabetical value and in form alpha@alpha.alpha.\n"
                          "   phone (str): Phone number in numerical value.\n"
                          "   company (str): Customer's company in alphabetical value.")
@click.pass_context
@click.argument('firstname', type=str)
@click.argument('lastname', type=str)
@click.argument('email', type=str)
@click.argument('phone', type=str)
@click.argument('company', type=str)
def create(ctx, firstname, lastname, email, phone, company):
    try:
        session = ctx.obj
        create_func(session, firstname, lastname, email, phone, company)
    except Exception as e:
        display_message_error(str(e))


@customer.command(help="Get a list of customers\n\n"
                          "Options:\n"
                          "   --mine (bool): If you are seller, filter awarded customers: True, not this filter: False.")
@click.option('--mine', type=bool, default=False, help="If you are seller, filter awarded customers: True, not this filter: False.")
@click.pass_context
def read(ctx, mine):
    try:
        session = ctx.obj
        read_func(session, mine)
    except Exception as e:
        display_message_error(str(e))


@customer.command(help="Get a customer with his ID\n\n"
                          "Parameters:\n"
                          "   customer_id (int): Customer ID in numerical value.")
@click.argument('customer_id', type=int)
@click.pass_context
def getbyid(ctx, customer_id):
    try:
        session = ctx.obj
        get_by_id_func(session, customer_id)
    except Exception as e:
        display_message_error(str(e))


@customer.command(help="Get a customer with his email\n\n"
                          "Parameters:\n"
                          "   customer_email (str): Customer Email in alphabetical value and in form alpha@alpha.alpha.")
@click.argument('customer_email', type=str)
@click.pass_context
def getbyemail(ctx, customer_email):
    try:
        session = ctx.obj
        get_by_email_func(session, customer_email)
    except Exception as e:
        display_message_error(str(e))


@customer.command(help="Update a customer\n\n"
                          "Parameters:\n"
                          "   customer_id (int): Customer ID in numerical value.\n"
                          "Options:\n"
                          "   --firstname (str): For change: Firstname in alphabetical value, for keep unchanged: None.\n"
                          "   --lastname (str): For change: Lastname in alphabetical value, for keep unchanged: None.\n"
                          "   --email (str): For change: Email in alphabetical value and in form alpha@alpha.alpha, for keep unchanged: None.\n"
                          "   --phone (str): For change: Phone number in numerical value, for keep unchanged: None.\n"
                          "   --company (str): For change: Customer's company in alphabetical value, for keep unchanged: None.")
@click.pass_context
@click.argument('customer_id', type=int)
@click.option('--firstname', type=str, default=None, help="For change: Firstname in alphabetical value, for keep unchanged: None.")
@click.option('--lastname', type=str, default=None, help="For change: Lastname in alphabetical value, for keep unchanged: None.")
@click.option('--email', type=str, default=None, help="For change: Email in alphabetical value and in form alpha@alpha.alpha, for keep unchanged: None.")
@click.option('--phone', type=str, default=None, help="For change: Phone number in numerical value, for keep unchanged: None.")
@click.option('--company', type=str, default=None, help="For change: Customer's compagny in alphabetical value, for keep unchanged: None.")
def update(ctx, customer_id, firstname, lastname, email, phone, company):
    try:
        session = ctx.obj
        update_func(session, customer_id, firstname, lastname, email, phone, company)
    except Exception as e:
        display_message_error(str(e))


@customer.command(help="Delete a customer\n\n"
                          "Parameters:\n"
                          "   customer_id (int): Customer ID in numerical value.")
@click.argument('customer_id', type=int)
@click.pass_context
def delete(ctx, customer_id):
    try:
        session = ctx.obj
        delete_func(session, customer_id)
    except Exception as e:
        display_message_error(str(e))
