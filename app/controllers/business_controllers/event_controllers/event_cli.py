import click
from .event_controller import create_func, read_func, get_by_id_func, update_func, delete_func
from app.views.general_views.generic_message import display_message_info, display_message_error
from datetime import datetime


@click.group(help="Event forms command group")
def eventform():
    pass


@eventform.command(help="Create an event with form")
@click.pass_context
def createform(ctx):
    try:
        session = ctx.obj
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
        create_func(session, name, event_start, event_end, location, attendees, instruction, contract)
    except Exception as e:
        display_message_error(str(e))


@eventform.command(help="Get a list of events with form")
@click.pass_context
def readform(ctx):
    try:
        session = ctx.obj
        display_message_info("If you are support, filter awarded events: True, not this filter: False.")
        mine = click.prompt("Mine", type=click.BOOL, default=False)
        display_message_info("Filter only contracts with support assigned: True, without support assigned: False, both: None.")
        is_supported = click.prompt("Is_Supported", type=click.BOOL, default=None)
        read_func(session, mine, is_supported)
    except Exception as e:
        display_message_error(str(e))


@eventform.command(help="Get an event with his ID with form")
@click.pass_context
def getbyidform(ctx):
    try:
        session = ctx.obj
        display_message_info("Event ID in numerical value.")
        event_id = click.prompt("Event_Id", type=click.INT)
        get_by_id_func(session, event_id)
    except Exception as e:
        display_message_error(str(e))


@eventform.command(help="Update an event with form")
@click.pass_context
def updateform(ctx):
    try:
        session = ctx.obj
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
        update_func(session, event_id, name, event_start, event_end, location, attendees, instruction, contract, support)
    except Exception as e:
        display_message_error(str(e))


@eventform.command(help="Delete an event with form")
@click.pass_context
def deleteform(ctx):
    try:
        session = ctx.obj
        display_message_info("Event ID in numerical value.")
        event_id = click.prompt("Event_Id", type=click.INT)
        delete_func(session, event_id)
    except Exception as e:
        display_message_error(str(e))


@click.group(help="Event command group")
def event():
    pass


@event.command(help="Create an event\n\n"
                     "Parameters:\n"
                     "   name (str): Event Name in alphabetical value.\n"
                     "   event_start (datetime): Event start date in this form: YYYY-MM-DD HH:MM:SS.\n"
                     "   event_end (datetime): Event end date in this form: YYYY-MM-DD HH:MM:SS.\n"
                     "   location (str): Event location in alphabetical value.\n"
                     "   attendees (int): Attendees amount in numerical value.\n"
                     "   instruction (str): Some instructions for the event in alphabetical value.\n"
                     "   contract (int): Contract Id in numerical value.")
@click.pass_context
@click.argument('name', type=str)
@click.argument('event_start', type=datetime)
@click.argument('event_end', type=datetime)
@click.argument('location', type=str)
@click.argument('attendees', type=int)
@click.argument('instruction', type=str)
@click.argument('contract', type=int)
def create(ctx, name, event_start, event_end, location, attendees, instruction, contract):
    try:
        session = ctx.obj
        create_func(session, name, event_start, event_end, location, attendees, instruction, contract)
    except Exception as e:
        display_message_error(str(e))


@event.command(help="Get a list of events\n\n"
                     "Options:\n"
                     "   --mine (bool): If you are support, filter awarded events: True, not this filter: False.\n"
                     "   --is_supported (bool): Filter only contracts with support assigned: True, without support assigned: False, both: None.")
@click.option('--mine', type=bool, default=False, help="If you are support, filter awarded events: True, not this filter: False.")
@click.option('--is_supported', type=bool, default=None, help="Filter only contracts with support assigned: True, without support assigned: False, both: None.")
@click.pass_context
def read(ctx, mine, is_supported):
    try:
        session = ctx.obj
        read_func(session, mine, is_supported)
    except Exception as e:
        display_message_error(str(e))


@event.command(help="Get an event with his ID\n\n"
                     "Parameters:\n"
                     "   event_id (int): Event ID in numerical value.")
@click.argument('event_id', type=int)
@click.pass_context
def getbyid(ctx, event_id):
    try:
        session = ctx.obj
        get_by_id_func(session, event_id)
    except Exception as e:
        display_message_error(str(e))


@event.command(help="Update an event\n\n"
                     "Parameters:\n"
                     "   event_id (int): Event ID in numerical value.\n"
                     "Options:\n"
                     "   --name (str): For change: Event Name in alphabetical value, for keep unchanged: None.\n"
                     "   --event_start (datetime): For change: Event start date in this form: YYYY-MM-DD HH:MM:SS, for keep unchanged: None.\n"
                     "   --event_end (datetime): For change: Event end date in this form: YYYY-MM-DD HH:MM:SS, for keep unchanged: None.\n"
                     "   --location (str): For change: Event location in alphabetical value, for keep unchanged: None.\n"
                     "   --attendees (int): For change: Attendees amount in numerical value, for keep unchanged: None.\n"
                     "   --instruction (str): For change: Some instructions for the event in alphabetical value, for keep unchanged: None.\n"
                     "   --contract (int): For change: Contract Id in numerical value, for keep unchanged: None.\n"
                     "   --support (int): For change: Support Id in numerical value, for keep unchanged: None.")
@click.pass_context
@click.argument('event_id', type=int)
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
        update_func(session, event_id, name, event_start, event_end, location, attendees, instruction, contract, support)
    except Exception as e:
        display_message_error(str(e))


@event.command(help="Delete an event\n\n"
                     "Parameters:\n"
                     "   event_id (int): Event ID in numerical value.")
@click.argument('event_id', type=int)
@click.pass_context
def delete(ctx, event_id):
    try:
        session = ctx.obj
        delete_func(session, event_id)
    except Exception as e:
        display_message_error(str(e))
