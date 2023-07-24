from rich.console import Console

console = Console()


def display_event(event):
    console.print("[bold green]Event Details:[/bold green]")
    console.print(f"ID: {event.id}")
    console.print(f"Name: {event.name}")
    console.print(f"Start Time: {event.event_start}")
    console.print(f"End Time: {event.event_end}")
    console.print(f"Location: {event.location}")
    console.print(f"Number of Attendees: {event.attendees}")
    console.print(f"Instruction: {event.instruction}")
    if event.collaborator:
        console.print(f"Collaborator: {event.collaborator.firstname} {event.collaborator.lastname}")
    else:
        console.print("Collaborator: None")
    if event.contract:
        console.print("Contract:")
        console.print(f"  ID: {event.contract.id}")
        console.print(f"  Type: {event.contract.type}")
        console.print(f"  Start Date: {event.contract.start_date}")
        console.print(f"  End Date: {event.contract.end_date}")
    else:
        console.print("Contract: None")
