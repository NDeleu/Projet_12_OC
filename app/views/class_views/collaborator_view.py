from rich.console import Console
from rich.table import Table
from app.models.class_models.user_models.collaborator_model import Collaborator

console = Console()


def display_collaborator_detail(collaborator):
    console.print("[bold yellow]Collaborator Details:[/bold yellow]")
    console.print(f"Collaborator ID: {collaborator.id}")
    console.print(f"Firstname: {collaborator.firstname}")
    console.print(f"Lastname: {collaborator.lastname}")
    if collaborator.role == Collaborator.RoleEnum.administrator:
        collaborator_role = "Administrator"
    elif collaborator.role == Collaborator.RoleEnum.seller:
        collaborator_role = "Seller"
    elif collaborator.role == Collaborator.RoleEnum.support:
        collaborator_role = "Support"
    else:
        collaborator_role = "Unknown"
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


def display_collaborator_summary(collaborator):
    collaborator_id = f"{collaborator.id}"
    collaborator_firstname = f"{collaborator.firstname}"
    collaborator_lastname = f"{collaborator.lastname}"
    if collaborator.role == Collaborator.RoleEnum.administrator:
        collaborator_role = "Administrator"
    elif collaborator.role == Collaborator.RoleEnum.seller:
        collaborator_role = "Seller"
    elif collaborator.role == Collaborator.RoleEnum.support:
        collaborator_role = "Support"
    else:
        collaborator_role = "Unknown"
    collaborator_email = f"{collaborator.email}"

    collaborator_summary = f"{collaborator_id}, {collaborator_firstname}, {collaborator_lastname}, {collaborator_role}, {collaborator_email}"
    return collaborator_summary


def display_list_contracts(collaborators):
    table = Table(title="[bold yellow]Collaborators List:[/bold yellow]")

    table.add_column("ID")
    table.add_column("Firstname")
    table.add_column("Lastname")
    table.add_column("Role")
    table.add_column("Email")

    for collaborator in collaborators:
        formatted_collaborator = display_collaborator_summary(collaborator)
        table.add_row(*formatted_collaborator.split(", "))

    console.print(table)
