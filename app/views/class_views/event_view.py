from rich.console import Console
from rich.table import Table

console = Console()


def display_event_detail(event):
    console.print("[bold yellow]Event Details:[/bold yellow]")
    console.print(f"Event ID: {event.id}")
    console.print(f"Name: {event.name}")
    console.print(f"Start Time: {event.event_start}")
    console.print(f"End Time: {event.event_end}")
    console.print(f"Location: {event.location}")
    console.print(f"Number of Attendees: {event.attendees}")
    console.print(f"Instruction: {event.instruction}")
    if event.contract:
        console.print("Contract:")
        console.print(f"  Contract ID: {event.contract.id}")
        console.print(f"  Date Created: {event.contract.date_created}")
    else:
        console.print("Contract: None")
    if event.contract.customer:
        console.print("Customer:")
        console.print(f"  Customer ID: {event.contract.customer_id}")
        console.print(f"  Customer Name: {event.contract.customer.firstname} - {event.contract.customer.lastname}")
        console.print(f"  Customer Email: {event.contract.customer.email}")
        console.print(f"  Customer Phone: {event.contract.customer.phone}")
    else:
        console.print("Customer: None")
    if event.collaborator:
        console.print("Support assigned:")
        console.print(f"  Support Name assigned: {event.collaborator.firstname} - {event.collaborator.lastname}")
        console.print(f"  Support Email assigned: {event.collaborator.email}")
    else:
        console.print("Support assigned: None")


def display_event_summary(event):
    event_id = f"{event.id}"
    event_name = f"{event.name}"
    event_start = f"{event.event_start}"
    event_end = f"{event.event_end}"
    event_location = f"{event.location}"
    if event.contract.customer:
        event_customer_email = f"{event.contract.customer.email}"
    else:
        event_customer_email = "None"

    event_summary = f"{event_id}, {event_name}, {event_start}, {event_end}, {event_location}, {event_customer_email}"

    return event_summary


def display_list_events(events):
    table = Table(title="[bold yellow]Events List:[/bold yellow]")

    table.add_column("ID")
    table.add_column("Name")
    table.add_column("Start Time")
    table.add_column("End Time")
    table.add_column("Location")
    table.add_column("Customer Email")

    for event in events:
        formatted_event = display_event_summary(event)
        table.add_row(*formatted_event.split(", "))

    console.print(table)