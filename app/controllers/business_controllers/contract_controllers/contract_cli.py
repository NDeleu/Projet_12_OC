import click
from .contract_controller import create_func, read_func, get_by_id_func, update_func, delete_func


@click.group()
def contract_form():
    pass


@contract_form.command()
@click.pass_context
def create_form(ctx):
    session = ctx.obj
    user = None
    total_amount = click.prompt("Total_Amount", type=click.FLOAT)
    left_to_pay = click.prompt("Left_to_Pay", type=click.FLOAT)
    customer = click.prompt("Customer_Id", type=click.INT)
    signed = click.prompt("Signed", type=click.BOOL, default=False)
    create_func(session, user, total_amount, left_to_pay, customer, signed)


@contract_form.command()
@click.pass_context
def read_form(ctx):
    session = ctx.obj
    user = None
    mine = click.prompt("Mine", type=click.BOOL, default=False)
    is_signed = click.prompt("Is_Signed", type=click.BOOL, default=None)
    with_event = click.prompt("With_Event", type=click.BOOL, default=None)
    is_paid = click.prompt("Is_Paid", type=click.BOOL, default=None)
    read_func(session, user, mine, is_signed, with_event, is_paid)


@contract_form.command()
@click.pass_context
def get_by_id_form(ctx):
    session = ctx.obj
    user = None
    contract_id = click.prompt("Contract_Id", type=click.INT)
    get_by_id_func(session, user, contract_id)


@contract_form.command()
@click.pass_context
def update_form(ctx):
    session = ctx.obj
    user = None
    contract_id = click.prompt("Contract_Id", type=click.INT)
    total_amount = click.prompt("Total_Amount", type=click.FLOAT, default=None)
    left_to_pay = click.prompt("Left_to_Pay", type=click.FLOAT, default=None)
    signed = click.prompt("Signed", type=click.BOOL, default=False)
    update_func(session, user, contract_id, total_amount, left_to_pay, signed)


@contract_form.command()
@click.pass_context
def delete_form(ctx):
    session = ctx.obj
    user = None
    contract_id = click.prompt("Contract_Id", type=click.INT)
    delete_func(session, user, contract_id)


@click.group()
def contract():
    pass


@contract.command()
@click.pass_context
@click.argument('total_amount', type=float)
@click.argument('left_to_pay', type=float)
@click.argument('customer', type=int)
@click.argument('signed', type=bool, default=False)
def create(ctx, total_amount, left_to_pay, customer, signed):
    session = ctx.obj
    user = None
    create_func(session, user, total_amount, left_to_pay, customer, signed)


@contract.command()
@click.option('--mine', type=bool, default=False)
@click.option('--is_signed', type=bool, default=None)
@click.option('--with_event', type=bool, default=None)
@click.option('--is_paid', type=bool, default=None)
@click.pass_context
def read(ctx, mine, is_signed, with_event, is_paid):
    session = ctx.obj
    user = None
    read_func(session, user, mine, is_signed, with_event, is_paid)


@contract.command()
@click.argument('contract_id', type=int)
@click.pass_context
def get_by_id(ctx, contract_id):
    session = ctx.obj
    user = None
    get_by_id_func(session, user, contract_id)


@contract.command()
@click.pass_context
@click.argument('contract_id', type=int)
@click.option('--total_amount', type=float, default=None)
@click.option('--left_to_pay', type=float, default=None)
@click.option('--signed', type=bool, default=False)
def update(ctx, contract_id, total_amount, left_to_pay, signed):
    session = ctx.obj
    user = None
    update_func(session, user, contract_id, total_amount, left_to_pay, signed)


@contract.command()
@click.argument('contract_id', type=int)
@click.pass_context
def delete(ctx, contract_id):
    session = ctx.obj
    user = None
    delete_func(session, user, contract_id)
