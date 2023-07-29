import click
from .event_controller import create_func, read_func, get_by_id_func, update_func, delete_func
from app.views.general_views.generic_message import display_message_info, display_message_error
from datetime import datetime


def convert_input_to_datetime(input_string):
    formats_to_try = [
        "%Y/%m/%d-%H:%M:%S",
        "%Y/%m/%d-%H:%M",
        "%Y/%m/%d",
        "%d/%m/%Y-%H:%M:%S",
        "%d/%m/%Y-%H:%M",
        "%d/%m/%Y",
    ]

    for date_format in formats_to_try:
        try:
            date_time_obj = datetime.strptime(input_string, date_format)
            return date_time_obj
        except ValueError:
            pass

    raise ValueError("Unrecognized date format")


def convert_input_to_integer(input_string):
    try:
        int_obj = int(input_string)
        return int_obj
    except ValueError:
        pass

    raise ValueError("Input not suitable for an integer.")


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
        display_message_info("Event start date in this form: YYYY/MM/DD-HH:MM:SS.")
        event_start = click.prompt("Event_Start", type=click.STRING)
        event_start = convert_input_to_datetime(event_start)
        display_message_info("Event end date in this form: YYYY/MM/DD-HH:MM:SS.")
        event_end = click.prompt("Event_End", type=click.STRING)
        event_end = convert_input_to_datetime(event_end)
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
        display_message_info("Filter only contracts with support assigned: True, without support assigned: False, both: Both.")
        is_supported = click.prompt("Is_Supported", type=click.STRING, default="Both")
        if is_supported == "Both":
            is_supported = None
        elif is_supported == "True":
            is_supported = True
        elif is_supported == "False":
            is_supported = False
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
        if name == "None":
            name = None
        display_message_info("For change: Event start date in this form: YYYY/MM/DD-HH:MM:SS, for keep unchanged: None.")
        event_start = click.prompt("Event_Start", type=click.STRING, default=None)
        if event_start == "None":
            event_start = None
        if event_start is not None:
            event_start = convert_input_to_datetime(event_start)
        display_message_info("For change: Event end date in this form: YYYY/MM/DD-HH:MM:SS, for keep unchanged: None.")
        event_end = click.prompt("Event_End", type=click.STRING, default=None)
        if event_end == "None":
            event_end = None
        if event_end is not None:
            event_end = convert_input_to_datetime(event_end)
        display_message_info("For change: Event location in alphabetical value, for keep unchanged: None.")
        location = click.prompt("Location", type=click.STRING, default=None)
        if location == "None":
            location = None
        display_message_info("For change: Attendees amount in numerical value, for keep unchanged: None.")
        attendees = click.prompt("Attendees", type=click.STRING, default=None)
        if attendees == "None":
            attendees = None
        if attendees is not None:
            attendees = convert_input_to_integer(attendees)
        display_message_info("For change: Some instructions for the event in alphabetical value, for keep unchanged: None.")
        instruction = click.prompt("Instruction", type=click.STRING, default=None)
        if instruction == "None":
            instruction = None
        display_message_info("For change: Contract Id in numerical value, for keep unchanged: None.")
        contract = click.prompt("Contract_Id", type=click.STRING, default=None)
        if contract == "None":
            contract = None
        if contract is not None:
            contract = convert_input_to_integer(contract)
        display_message_info("For change: Support Id in numerical value, for keep unchanged: None.")
        support = click.prompt("Support_Id", type=click.STRING, default=None)
        if support == "None":
            support = None
        if support is not None:
            support = convert_input_to_integer(support)
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


@event.command(help="Create an event\n\n\n"
                     "Parameters:\n\n"
                     "   name (str): Event Name in alphabetical value.\n\n"
                     "   event_start (datetime): Event start date in this form: YYYY/MM/DD-HH:MM:SS.\n\n"
                     "   event_end (datetime): Event end date in this form: YYYY/MM/DD-HH:MM:SS.\n\n"
                     "   location (str): Event location in alphabetical value.\n\n"
                     "   attendees (int): Attendees amount in numerical value.\n\n"
                     "   instruction (str): Some instructions for the event in alphabetical value.\n\n"
                     "   contract (int): Contract Id in numerical value.")
@click.pass_context
@click.argument('name', type=str)
@click.argument('event_start', type=str)
@click.argument('event_end', type=str)
@click.argument('location', type=str)
@click.argument('attendees', type=int)
@click.argument('instruction', type=str)
@click.argument('contract', type=int)
def create(ctx, name, event_start, event_end, location, attendees, instruction, contract):
    try:
        session = ctx.obj
        event_start = convert_input_to_datetime(event_start)
        event_end = convert_input_to_datetime(event_end)
        create_func(session, name, event_start, event_end, location, attendees, instruction, contract)
    except Exception as e:
        display_message_error(str(e))


@event.command(help="Get a list of events\n\n\n"
                     "Options:\n\n"
                     "   --mine (bool): If you are support, filter awarded events: True, not this filter: False.\n\n"
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


@event.command(help="Get an event with his ID\n\n\n"
                     "Parameters:\n\n"
                     "   event_id (int): Event ID in numerical value.")
@click.argument('event_id', type=int)
@click.pass_context
def getbyid(ctx, event_id):
    try:
        session = ctx.obj
        get_by_id_func(session, event_id)
    except Exception as e:
        display_message_error(str(e))


@event.command(help="Update an event\n\n\n"
                     "Parameters:\n\n"
                     "   event_id (int): Event ID in numerical value.\n\n"
                     "Options:\n\n"
                     "   --name (str): For change: Event Name in alphabetical value, for keep unchanged: None.\n\n"
                     "   --event_start (datetime): For change: Event start date in this form: YYYY/MM/DD-HH:MM:SS, for keep unchanged: None.\n\n"
                     "   --event_end (datetime): For change: Event end date in this form: YYYY/MM/DD-HH:MM:SS, for keep unchanged: None.\n\n"
                     "   --location (str): For change: Event location in alphabetical value, for keep unchanged: None.\n\n"
                     "   --attendees (int): For change: Attendees amount in numerical value, for keep unchanged: None.\n\n"
                     "   --instruction (str): For change: Some instructions for the event in alphabetical value, for keep unchanged: None.\n\n"
                     "   --contract (int): For change: Contract Id in numerical value, for keep unchanged: None.\n\n"
                     "   --support (int): For change: Support Id in numerical value, for keep unchanged: None.")
@click.pass_context
@click.argument('event_id', type=int)
@click.option('--name', type=str, default=None, help="For change: Event Name in alphabetical value, for keep unchanged: None.")
@click.option('--event_start', type=str, default=None, help="For change: Event start date in this form: YYYY/MM/DD-HH:MM:SS, for keep unchanged: None.")
@click.option('--event_end', type=str, default=None, help="For change: Event end date in this form: YYYY/MM/DD-HH:MM:SS, for keep unchanged: None.")
@click.option('--location', type=str, default=None, help="For change: Event location in alphabetical value, for keep unchanged: None.")
@click.option('--attendees', type=int, default=None, help="For change: Attendees amount in numerical value, for keep unchanged: None.")
@click.option('--instruction', type=str, default=None, help="For change: Some instructions for the event in alphabetical value, for keep unchanged: None.")
@click.option('--contract', type=int, default=None, help="For change: Contract Id in numerical value, for keep unchanged: None.")
@click.option('--support', type=int, default=None, help="For change: Support Id in numerical value, for keep unchanged: None.")
def update(ctx, event_id, name, event_start, event_end, location, attendees, instruction, contract, support):
    try:
        session = ctx.obj
        if event_start is not None:
            event_start = convert_input_to_datetime(event_start)
        if event_end is not None:
            event_end = convert_input_to_datetime(event_end)
        update_func(session, event_id, name, event_start, event_end, location, attendees, instruction, contract, support)
    except Exception as e:
        display_message_error(str(e))


@event.command(help="Delete an event\n\n\n"
                     "Parameters:\n\n"
                     "   event_id (int): Event ID in numerical value.")
@click.argument('event_id', type=int)
@click.pass_context
def delete(ctx, event_id):
    try:
        session = ctx.obj
        delete_func(session, event_id)
    except Exception as e:
        display_message_error(str(e))
