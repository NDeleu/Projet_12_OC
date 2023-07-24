import click
from .event_controller import create_func, read_func, get_by_id_func, update_func, delete_func
from datetime import datetime


@click.group()
def event_form():
    pass


@event_form.command()
@click.pass_context
def create_form(ctx):
    session = ctx.obj
    user = None
    name = click.prompt("Name", type=click.STRING)
    event_start = click.prompt("Event_Start", type=click.DateTime)
    event_end = click.prompt("Event_End", type=click.DateTime)
    location = click.prompt("Location", type=click.STRING)
    attendees = click.prompt("Attendees", type=click.INT)
    instruction = click.prompt("Instruction", type=click.STRING)
    contract = click.prompt("Contract_Id", type=click.INT)
    create_func(session, user, name, event_start, event_end, location, attendees, instruction, contract)


@event_form.command()
@click.pass_context
def read_form(ctx):
    session = ctx.obj
    user = None
    mine = click.prompt("Mine", type=click.BOOL, default=False)
    is_supported = click.prompt("Is_Supported", type=click.BOOL, default=None)
    read_func(session, user, mine, is_supported)


@event_form.command()
@click.pass_context
def get_by_id_form(ctx):
    session = ctx.obj
    user = None
    event_id = click.prompt("Event_Id", type=click.INT)
    get_by_id_func(session, user, event_id)


@event_form.command()
@click.pass_context
def update_form(ctx):
    session = ctx.obj
    user = None
    event_id = click.prompt("Event_Id", type=click.INT)
    name = click.prompt("Name", type=click.STRING, default=None)
    event_start = click.prompt("Event_Start", type=click.DateTime, default=None)
    event_end = click.prompt("Event_End", type=click.DateTime, default=None)
    location = click.prompt("Location", type=click.STRING, default=None)
    attendees = click.prompt("Attendees", type=click.INT, default=None)
    instruction = click.prompt("Instruction", type=click.STRING, default=None)
    contract = click.prompt("Contract_Id", type=click.INT, default=None)
    support = click.prompt("Support_Id", type=click.INT, default=None)
    update_func(session, user, event_id, name, event_start, event_end, location, attendees, instruction, contract, support)


@event_form.command()
@click.pass_context
def delete_form(ctx):
    session = ctx.obj
    user = None
    event_id = click.prompt("Event_Id", type=click.INT)
    delete_func(session, user, event_id)


@click.group()
def event():
    pass


@event.command()
@click.pass_context
@click.argument('name', type=str)
@click.argument('event_start', type=datetime)
@click.argument('event_end', type=datetime)
@click.argument('location', type=str)
@click.argument('attendees', type=int)
@click.argument('instruction', type=str)
@click.argument('contract', type=int)
def create(ctx, name, event_start, event_end, location, attendees, instruction, contract):
    session = ctx.obj
    user = None
    create_func(session, user, name, event_start, event_end, location, attendees, instruction, contract)


@event.command()
@click.option('--mine', type=bool, default=False)
@click.option('--is_supported', type=bool, default=None)
@click.pass_context
def read(ctx, mine, is_supported):
    session = ctx.obj
    user = None
    read_func(session, user, mine, is_supported)


@event.command()
@click.argument('event_id', type=int)
@click.pass_context
def get_by_id(ctx, event_id):
    session = ctx.obj
    user = None
    get_by_id_func(session, user, event_id)


@event.command()
@click.pass_context
@click.argument('event_id', type=int)
@click.option('--name', type=str, default=None)
@click.option('--event_start', type=datetime, default=None)
@click.option('--event_end', type=datetime, default=None)
@click.option('--location', type=str, default=None)
@click.option('--attendees', type=int, default=None)
@click.option('--instruction', type=str, default=None)
@click.option('--contract', type=int, default=None)
@click.option('--support', type=int, default=None)
def update(ctx, event_id, name, event_start, event_end, location, attendees, instruction, contract, support):
    session = ctx.obj
    user = None
    update_func(session, user, event_id, name, event_start, event_end, location, attendees, instruction, contract, support)


@event.command()
@click.argument('event_id', type=int)
@click.pass_context
def delete(ctx, event_id):
    session = ctx.obj
    user = None
    delete_func(session, user, event_id)
