from rich.console import Console
from app.models.class_models.user_models.collaborator_model import Collaborator

console = Console()


def display_collaborator_detail(collaborator):
    console.print("[bold yellow]Collaborator Details:[/bold yellow]")
    console.print(f"Collaborator ID: {collaborator.id}")
    console.print(f"Firstname: {collaborator.firstname}")
    console.print(f"Lastname: {collaborator.lastname}")
    console.print(f"Role: {collaborator.role}")
    console.print(f"Email: {collaborator.email}")
    if collaborator.role == Collaborator.RoleEnum.support:
        list_events = collaborator.events
        if list_events:
            console.print("Events:")
            for event in list_events:
                console.print(f"  Event ID: {event.id}")
                console.print(f"  Event Name: {event.name}")
        else:
            console.print("Events: None")
    elif collaborator.role == Collaborator.RoleEnum.seller:
        list_customers = collaborator.customers
        if list_customers:
            console.print("Customer:")
            for customer in list_customers:
                console.print(f"  Customer ID: {customer.id}")
                console.print(f"  Customer Name: {customer.firstname} - {customer.lastname}")
                console.print(f"  Customer Email: {customer.email}")
        else:
            console.print("Customers: None")


def display_announce_collaborator_list():
    console.print("[bold yellow]Collaborator List:[/bold yellow]")


def display_collaborator_summary(collaborator):
    console.print(" ")
    console.print(f"ID: {collaborator.id}")
    console.print(f"Name: {collaborator.firstname} - {collaborator.lastname}")
    console.print(f"Role: {collaborator.role}")
    console.print(f"Email: {collaborator.email}")
