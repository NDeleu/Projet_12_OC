import click
from .contract_controller import create_func, read_func, get_by_id_func, update_func, delete_func
from app.views.general_views.generic_message import display_message_info, display_message_error


@click.group(help="Contract forms command group")
def contract_form():
    pass


@contract_form.command(help="Create a contract with form")
@click.pass_context
def create_form(ctx):
    try:
        session = ctx.obj
        user = None
        display_message_info("Total contract amount in numerical value.")
        total_amount = click.prompt("Total_Amount", type=click.FLOAT)
        display_message_info("Left to pay in numerical value.")
        left_to_pay = click.prompt("Left_to_Pay", type=click.FLOAT)
        display_message_info("Customer ID in numerical value.")
        customer = click.prompt("Customer_Id", type=click.INT)
        display_message_info("Contract signed, for yes: True, for no: False.")
        signed = click.prompt("Signed", type=click.BOOL, default=False)
        create_func(session, user, total_amount, left_to_pay, customer, signed)
    except Exception as e:
        display_message_error(str(e))


@contract_form.command(help="Get a list of contracts with form")
@click.pass_context
def read_form(ctx):
    try:
        session = ctx.obj
        user = None
        display_message_info("If you are seller, filter awarded contracts: True, not this filter: False.")
        mine = click.prompt("Mine", type=click.BOOL, default=False)
        display_message_info("Filter only contracts signed: True, not signed: False, both: None.")
        is_signed = click.prompt("Is_Signed", type=click.BOOL, default=None)
        display_message_info("Filter only contracts with existing event: True, without existing event: False, both: None.")
        with_event = click.prompt("With_Event", type=click.BOOL, default=None)
        display_message_info("Filter only contracts paid: True, not paid: False, both: None.")
        is_paid = click.prompt("Is_Paid", type=click.BOOL, default=None)
        read_func(session, user, mine, is_signed, with_event, is_paid)
    except Exception as e:
        display_message_error(str(e))


@contract_form.command(help="Get a contract with his ID with form")
@click.pass_context
def get_by_id_form(ctx):
    try:
        session = ctx.obj
        user = None
        display_message_info("Contract ID in numerical value.")
        contract_id = click.prompt("Contract_Id", type=click.INT)
        get_by_id_func(session, user, contract_id)
    except Exception as e:
        display_message_error(str(e))


@contract_form.command(help="Update a contract with form")
@click.pass_context
def update_form(ctx):
    try:
        session = ctx.obj
        user = None
        display_message_info("Contract ID in numerical value.")
        contract_id = click.prompt("Contract_Id", type=click.INT)
        display_message_info("For change: Total contract amount in numerical value, for keep unchanged: None.")
        total_amount = click.prompt("Total_Amount", type=click.FLOAT, default=None)
        display_message_info("For change: Left to pay in numerical value, for keep unchanged: None.")
        left_to_pay = click.prompt("Left_to_Pay", type=click.FLOAT, default=None)
        display_message_info("Contract signed, for yes: True, for no: False.")
        signed = click.prompt("Signed", type=click.BOOL, default=False)
        update_func(session, user, contract_id, total_amount, left_to_pay, signed)
    except Exception as e:
        display_message_error(str(e))


@contract_form.command(help="Delete a contract with form")
@click.pass_context
def delete_form(ctx):
    try:
        session = ctx.obj
        user = None
        display_message_info("Contract ID in numerical value.")
        contract_id = click.prompt("Contract_Id", type=click.INT)
        delete_func(session, user, contract_id)
    except Exception as e:
        display_message_error(str(e))


@click.group(help="Contract command group")
def contract():
    pass


@contract.command(help="Create a contract")
@click.pass_context
@click.argument('total_amount', type=float, help="Total contract amount in numerical value.")
@click.argument('left_to_pay', type=float, help="Left to pay in numerical value.")
@click.argument('customer', type=int, help="Customer ID in numerical value.")
@click.argument('signed', type=bool, default=False, help="Contract signed, for yes: True, for no: False.")
def create(ctx, total_amount, left_to_pay, customer, signed):
    try:
        session = ctx.obj
        user = None
        create_func(session, user, total_amount, left_to_pay, customer, signed)
    except Exception as e:
        display_message_error(str(e))


@contract.command(help="Get a list of contracts")
@click.option('--mine', type=bool, default=False, help="If you are seller, filter awarded contracts: True, not this filter: False.")
@click.option('--is_signed', type=bool, default=None, help="Filter only contracts signed: True, not signed: False, both: None.")
@click.option('--with_event', type=bool, default=None, help="Filter only contracts with existing event: True, without existing event: False, both: None.")
@click.option('--is_paid', type=bool, default=None, help="Filter only contracts paid: True, not paid: False, both: None.")
@click.pass_context
def read(ctx, mine, is_signed, with_event, is_paid):
    try:
        session = ctx.obj
        user = None
        read_func(session, user, mine, is_signed, with_event, is_paid)
    except Exception as e:
        display_message_error(str(e))


@contract.command(help="Get a contract with his ID")
@click.argument('contract_id', type=int, help="Contract ID in numerical value.")
@click.pass_context
def get_by_id(ctx, contract_id):
    try:
        session = ctx.obj
        user = None
        get_by_id_func(session, user, contract_id)
    except Exception as e:
        display_message_error(str(e))


@contract.command(help="Update a contract")
@click.pass_context
@click.argument('contract_id', type=int, help="Contract ID in numerical value.")
@click.option('--total_amount', type=float, default=None, help="For change: Total contract amount in numerical value, for keep unchanged: None.")
@click.option('--left_to_pay', type=float, default=None, help="For change: Left to pay in numerical value, for keep unchanged: None.")
@click.option('--signed', type=bool, default=False, help="Contract signed, for yes: True, for no: False.")
def update(ctx, contract_id, total_amount, left_to_pay, signed):
    try:
        session = ctx.obj
        user = None
        update_func(session, user, contract_id, total_amount, left_to_pay, signed)
    except Exception as e:
        display_message_error(str(e))


@contract.command(help="Delete a contract")
@click.argument('contract_id', type=int, help="Contract ID in numerical value.")
@click.pass_context
def delete(ctx, contract_id):
    try:
        session = ctx.obj
        user = None
        delete_func(session, user, contract_id)
    except Exception as e:
        display_message_error(str(e))
