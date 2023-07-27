import click
from .contract_controller import create_func, read_func, get_by_id_func, update_func, delete_func
from app.views.general_views.generic_message import display_message_info, display_message_error


@click.group(help="Contract forms command group")
def contractform():
    pass


@contractform.command(help="Create a contract with form")
@click.pass_context
def createform(ctx):
    try:
        session = ctx.obj
        display_message_info("Total contract amount in numerical value.")
        total_amount = click.prompt("Total_Amount", type=click.FLOAT)
        display_message_info("Left to pay in numerical value.")
        left_to_pay = click.prompt("Left_to_Pay", type=click.FLOAT)
        display_message_info("Customer ID in numerical value.")
        customer = click.prompt("Customer_Id", type=click.INT)
        display_message_info("Contract signed, for yes: True, for no: False.")
        signed = click.prompt("Signed", type=click.BOOL, default=False)
        create_func(session, total_amount, left_to_pay, customer, signed)
    except Exception as e:
        display_message_error(str(e))


@contractform.command(help="Get a list of contracts with form")
@click.pass_context
def readform(ctx):
    try:
        session = ctx.obj
        display_message_info("If you are seller, filter awarded contracts: True, not this filter: False.")
        mine = click.prompt("Mine", type=click.BOOL, default=False)
        display_message_info("Filter only contracts signed: True, not signed: False, both: Both.")
        is_signed = click.prompt("Is_Signed", type=click.STRING, default="Both")
        if is_signed == "Both":
            is_signed = None
        elif is_signed == "True":
            is_signed = True
        elif is_signed == "False":
            is_signed = False
        display_message_info("Filter only contracts with existing event: True, without existing event: False, both: Both.")
        with_event = click.prompt("With_Event", type=click.STRING, default="Both")
        if with_event == "Both":
            with_event = None
        elif with_event == "True":
            with_event = True
        elif with_event == "False":
            with_event = False
        display_message_info("Filter only contracts paid: True, not paid: False, both: Both.")
        is_paid = click.prompt("Is_Paid", type=click.STRING, default="Both")
        if is_paid == "Both":
            is_paid = None
        elif is_paid == "True":
            is_paid = True
        elif is_paid == "False":
            is_paid = False
        read_func(session, mine, is_signed, with_event, is_paid)
    except Exception as e:
        display_message_error(str(e))


@contractform.command(help="Get a contract with his ID with form")
@click.pass_context
def getbyidform(ctx):
    try:
        session = ctx.obj
        display_message_info("Contract ID in numerical value.")
        contract_id = click.prompt("Contract_Id", type=click.INT)
        get_by_id_func(session, contract_id)
    except Exception as e:
        display_message_error(str(e))


@contractform.command(help="Update a contract with form")
@click.pass_context
def updateform(ctx):
    try:
        session = ctx.obj
        display_message_info("Contract ID in numerical value.")
        contract_id = click.prompt("Contract_Id", type=click.INT)
        display_message_info("For change: Total contract amount in numerical value, for keep unchanged: None.")
        total_amount = click.prompt("Total_Amount", type=click.FLOAT, default=None)
        display_message_info("For change: Left to pay in numerical value, for keep unchanged: None.")
        left_to_pay = click.prompt("Left_to_Pay", type=click.FLOAT, default=None)
        display_message_info("Contract signed, for yes: True, for no: False.")
        signed = click.prompt("Signed", type=click.BOOL, default=False)
        update_func(session, contract_id, total_amount, left_to_pay, signed)
    except Exception as e:
        display_message_error(str(e))


@contractform.command(help="Delete a contract with form")
@click.pass_context
def deleteform(ctx):
    try:
        session = ctx.obj
        display_message_info("Contract ID in numerical value.")
        contract_id = click.prompt("Contract_Id", type=click.INT)
        delete_func(session, contract_id)
    except Exception as e:
        display_message_error(str(e))


@click.group(help="Contract command group")
def contract():
    pass


@contract.command(help="Create a contract\n\n"
                       "Parameters:\n"
                       "   total_amount (float): Total contract amount in numerical value.\n"
                       "   left_to_pay (float): Left to pay in numerical value.\n"
                       "   customer (int): Customer ID in numerical value.\n"
                       "   signed (bool): Contract signed, for yes: True, for no: False.")
@click.pass_context
@click.argument('total_amount', type=float)
@click.argument('left_to_pay', type=float)
@click.argument('customer', type=int)
@click.argument('signed', type=bool, default=False)
def create(ctx, total_amount, left_to_pay, customer, signed):
    try:
        session = ctx.obj
        create_func(session, total_amount, left_to_pay, customer, signed)
    except Exception as e:
        display_message_error(str(e))


@contract.command(help="Get a list of contracts\n\n"
                       "Options:\n"
                       "   --mine (bool): If you are seller, filter awarded contracts: True, not this filter: False.\n"
                       "   --is_signed (bool): Filter only contracts signed: True, not signed: False, both: None.\n"
                       "   --with_event (bool): Filter only contracts with existing event: True, without existing event: False, both: None.\n"
                       "   --is_paid (bool): Filter only contracts paid: True, not paid: False, both: None.")
@click.option('--mine', type=bool, default=False, help="If you are seller, filter awarded contracts: True, not this filter: False.")
@click.option('--is_signed', type=bool, default=None, help="Filter only contracts signed: True, not signed: False, both: None.")
@click.option('--with_event', type=bool, default=None, help="Filter only contracts with existing event: True, without existing event: False, both: None.")
@click.option('--is_paid', type=bool, default=None, help="Filter only contracts paid: True, not paid: False, both: None.")
@click.pass_context
def read(ctx, mine, is_signed, with_event, is_paid):
    try:
        session = ctx.obj
        read_func(session, mine, is_signed, with_event, is_paid)
    except Exception as e:
        display_message_error(str(e))


@contract.command(help="Get a contract with his ID\n\n"
                       "Parameters:\n"
                       "   contract_id (int): Contract ID in numerical value.")
@click.argument('contract_id', type=int)
@click.pass_context
def getbyid(ctx, contract_id):
    try:
        session = ctx.obj
        get_by_id_func(session, contract_id)
    except Exception as e:
        display_message_error(str(e))


@contract.command(help="Update a contract\n\n"
                       "Parameters:\n"
                       "   contract_id (int): Contract ID in numerical value.\n"
                       "Options:\n"
                       "   --total_amount (float): For change: Total contract amount in numerical value, for keep unchanged: None.\n"
                       "   --left_to_pay (float): For change: Left to pay in numerical value, for keep unchanged: None.\n"
                       "   --signed (bool): Contract signed, for yes: True, for no: False.")
@click.pass_context
@click.argument('contract_id', type=int)
@click.option('--total_amount', type=float, default=None, help="For change: Total contract amount in numerical value, for keep unchanged: None.")
@click.option('--left_to_pay', type=float, default=None, help="For change: Left to pay in numerical value, for keep unchanged: None.")
@click.option('--signed', type=bool, default=False, help="Contract signed, for yes: True, for no: False.")
def update(ctx, contract_id, total_amount, left_to_pay, signed):
    try:
        session = ctx.obj
        update_func(session, contract_id, total_amount, left_to_pay, signed)
    except Exception as e:
        display_message_error(str(e))


@contract.command(help="Delete a contract\n\n"
                       "Parameters:\n"
                       "   contract_id (int): Contract ID in numerical value.")
@click.argument('contract_id', type=int)
@click.pass_context
def delete(ctx, contract_id):
    try:
        session = ctx.obj
        delete_func(session, contract_id)
    except Exception as e:
        display_message_error(str(e))
