from rich.console import Console

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


def display_announce_event_list():
    console.print("[bold yellow]Events List:[/bold yellow]")


def display_event_summary(event):
    console.print(" ")
    console.print(f"Event ID: {event.id}")
    console.print(f"Name: {event.name}")
    console.print(f"Start Time: {event.event_start}")
    console.print(f"End Time: {event.event_end}")
    console.print(f"Location: {event.location}")
    if event.contract.customer:
        console.print(f"  Customer Email {event.contract.customer.email}")
    else:
        console.print("  Customer: None")
    if event.contract:
        console.print(f"  Contract ID: {event.contract.id}")
    else:
        console.print("  Contract: None")
    if event.collaborator:
        console.print(f"  Support Email assigned: {event.collaborator.email}")
    else:
        console.print("  Support assigned: None")
