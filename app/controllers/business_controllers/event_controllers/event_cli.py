import click
from .event_controller import create_func, read_func, get_by_id_func, update_func, delete_func
from app.views.general_views.generic_message import display_message_info, display_message_error
from datetime import datetime


@click.group(help="Event forms command group")
def event_form():
    pass


@event_form.command(help="Create an event with form")
@click.pass_context
def create_form(ctx):
    try:
        session = ctx.obj
        user = None
        display_message_info("Event Name in alphabetical value.")
        name = click.prompt("Name", type=click.STRING)
        display_message_info("Event start date in this form: YYYY-MM-DD HH:MM:SS.")
        event_start = click.prompt("Event_Start", type=click.DateTime)
        display_message_info("Event end date in this form: YYYY-MM-DD HH:MM:SS.")
        event_end = click.prompt("Event_End", type=click.DateTime)
        display_message_info("Event location in alphabetical value.")
        location = click.prompt("Location", type=click.STRING)
        display_message_info("Attendees amount in numerical value.")
        attendees = click.prompt("Attendees", type=click.INT)
        display_message_info("Some instructions for the event in alphabetical value.")
        instruction = click.prompt("Instruction", type=click.STRING)
        display_message_info("Contract Id in numerical value.")
        contract = click.prompt("Contract_Id", type=click.INT)
        create_func(session, user, name, event_start, event_end, location, attendees, instruction, contract)
    except Exception as e:
        display_message_error(str(e))


@event_form.command(help="Get a list of events with form")
@click.pass_context
def read_form(ctx):
    try:
        session = ctx.obj
        user = None
        display_message_info("If you are support, filter awarded events: True, not this filter: False.")
        mine = click.prompt("Mine", type=click.BOOL, default=False)
        display_message_info("Filter only contracts with support assigned: True, without support assigned: False, both: None.")
        is_supported = click.prompt("Is_Supported", type=click.BOOL, default=None)
        read_func(session, user, mine, is_supported)
    except Exception as e:
        display_message_error(str(e))


@event_form.command(help="Get an event with his ID with form")
@click.pass_context
def get_by_id_form(ctx):
    try:
        session = ctx.obj
        user = None
        display_message_info("Event ID in numerical value.")
        event_id = click.prompt("Event_Id", type=click.INT)
        get_by_id_func(session, user, event_id)
    except Exception as e:
        display_message_error(str(e))


@event_form.command(help="Update an event with form")
@click.pass_context
def update_form(ctx):
    try:
        session = ctx.obj
        user = None
        display_message_info("Event ID in numerical value.")
        event_id = click.prompt("Event_Id", type=click.INT)
        display_message_info("For change: Event Name in alphabetical value, for keep unchanged: None.")
        name = click.prompt("Name", type=click.STRING, default=None)
        display_message_info("For change: Event start date in this form: YYYY-MM-DD HH:MM:SS, for keep unchanged: None.")
        event_start = click.prompt("Event_Start", type=click.DateTime, default=None)
        display_message_info("For change: Event end date in this form: YYYY-MM-DD HH:MM:SS, for keep unchanged: None.")
        event_end = click.prompt("Event_End", type=click.DateTime, default=None)
        display_message_info("For change: Event location in alphabetical value, for keep unchanged: None.")
        location = click.prompt("Location", type=click.STRING, default=None)
        display_message_info("For change: Attendees amount in numerical value, for keep unchanged: None.")
        attendees = click.prompt("Attendees", type=click.INT, default=None)
        display_message_info("For change: Some instructions for the event in alphabetical value, for keep unchanged: None.")
        instruction = click.prompt("Instruction", type=click.STRING, default=None)
        display_message_info("For change: Contract Id in numerical value, for keep unchanged: None.")
        contract = click.prompt("Contract_Id", type=click.INT, default=None)
        display_message_info("For change: Support Id in numerical value, for keep unchanged: None.")
        support = click.prompt("Support_Id", type=click.INT, default=None)
        update_func(session, user, event_id, name, event_start, event_end, location, attendees, instruction, contract, support)
    except Exception as e:
        display_message_error(str(e))


@event_form.command(help="Delete an event with form")
@click.pass_context
def delete_form(ctx):
    try:
        session = ctx.obj
        user = None
        display_message_info("Event ID in numerical value.")
        event_id = click.prompt("Event_Id", type=click.INT)
        delete_func(session, user, event_id)
    except Exception as e:
        display_message_error(str(e))


@click.group(help="Event command group")
def event():
    pass


@event.command(help="Create an event")
@click.pass_context
@click.argument('name', type=str, help="Event Name in alphabetical value.")
@click.argument('event_start', type=datetime, help="Event start date in this form: YYYY-MM-DD HH:MM:SS.")
@click.argument('event_end', type=datetime, help="Event end date in this form: YYYY-MM-DD HH:MM:SS.")
@click.argument('location', type=str, help="Event location in alphabetical value.")
@click.argument('attendees', type=int, help="Attendees amount in numerical value.")
@click.argument('instruction', type=str, help="Some instructions for the event in alphabetical value.")
@click.argument('contract', type=int, help="Contract Id in numerical value.")
def create(ctx, name, event_start, event_end, location, attendees, instruction, contract):
    try:
        session = ctx.obj
        user = None
        create_func(session, user, name, event_start, event_end, location, attendees, instruction, contract)
    except Exception as e:
        display_message_error(str(e))


@event.command(help="Get a list of events")
@click.option('--mine', type=bool, default=False, help="If you are support, filter awarded events: True, not this filter: False.")
@click.option('--is_supported', type=bool, default=None, help="Filter only contracts with support assigned: True, without support assigned: False, both: None.")
@click.pass_context
def read(ctx, mine, is_supported):
    try:
        session = ctx.obj
        user = None
        read_func(session, user, mine, is_supported)
    except Exception as e:
        display_message_error(str(e))


@event.command(help="Get an event with his ID")
@click.argument('event_id', type=int, help="Event ID in numerical value.")
@click.pass_context
def get_by_id(ctx, event_id):
    try:
        session = ctx.obj
        user = None
        get_by_id_func(session, user, event_id)
    except Exception as e:
        display_message_error(str(e))


@event.command(help="Update an event")
@click.pass_context
@click.argument('event_id', type=int, help="Event ID in numerical value.")
@click.option('--name', type=str, default=None, help="For change: Event Name in alphabetical value, for keep unchanged: None.")
@click.option('--event_start', type=datetime, default=None, help="For change: Event start date in this form: YYYY-MM-DD HH:MM:SS, for keep unchanged: None.")
@click.option('--event_end', type=datetime, default=None, help="For change: Event end date in this form: YYYY-MM-DD HH:MM:SS, for keep unchanged: None.")
@click.option('--location', type=str, default=None, help="For change: Event location in alphabetical value, for keep unchanged: None.")
@click.option('--attendees', type=int, default=None, help="For change: Attendees amount in numerical value, for keep unchanged: None.")
@click.option('--instruction', type=str, default=None, help="For change: Some instructions for the event in alphabetical value, for keep unchanged: None.")
@click.option('--contract', type=int, default=None, help="For change: Contract Id in numerical value, for keep unchanged: None.")
@click.option('--support', type=int, default=None, help="For change: Support Id in numerical value, for keep unchanged: None.")
def update(ctx, event_id, name, event_start, event_end, location, attendees, instruction, contract, support):
    try:
        session = ctx.obj
        user = None
        update_func(session, user, event_id, name, event_start, event_end, location, attendees, instruction, contract, support)
    except Exception as e:
        display_message_error(str(e))


@event.command(help="Delete an event")
@click.argument('event_id', type=int, help="Event ID in numerical value.")
@click.pass_context
def delete(ctx, event_id):
    try:
        session = ctx.obj
        user = None
        delete_func(session, user, event_id)
    except Exception as e:
        display_message_error(str(e))
