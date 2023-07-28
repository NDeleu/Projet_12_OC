from rich.console import Console
from rich.table import Table

console = Console()


def display_customer_detail(customer):
    console.print("[bold yellow]Customer Details:[/bold yellow]")
    console.print(f"ID: {customer.id}")
    console.print(f"Firstname: {customer.firstname}")
    console.print(f"Lastname: {customer.lastname}")
    console.print(f"Email: {customer.email}")
    console.print(f"Phone: {customer.phone}")
    console.print(f"Company: {customer.company}")
    console.print(f"Creation Date: {customer.date_created}")
    console.print(f"Update Date: {customer.date_updated}")
    if customer.collaborator:
        console.print("Seller:")
        console.print(f"  Seller ID: {customer.collaborator_id}")
        console.print(f"  Seller Name: {customer.collaborator.firstname} - {customer.collaborator.lastname}")
        console.print(f"  Seller Email: {customer.collaborator.email}")
    else:
        console.print("Seller: None")
    list_contracts = customer.contracts
    if list_contracts:
        console.print("Contracts:")
        for contract in list_contracts:
            console.print(f"  Contract ID: {contract.id}")
            console.print(f"  Total Amount: {contract.total_amount}")
            console.print(f"  Left to Pay: {contract.left_to_pay}")
            console.print(f"  Date Created: {contract.date_created}")
            console.print(f"  Signed: {'Yes' if contract.signed else 'No'}")
            if contract.event:
                console.print("  Event:")
                console.print(f"    Event ID: {contract.event.id}")
                console.print(f"    Event Name: {contract.event.name}")
            else:
                console.print("  Event: None")
    else:
        console.print("Contracts: None")


def display_customer_summary(customer):
    customer_id = f"{customer.id}"
    customer_firstname = f"{customer.firstname}"
    customer_lastname = f"{customer.lastname}"
    customer_email = f"{customer.email}"
    customer_phone = f"{customer.phone}"
    customer_company = f"{customer.company}"
    if customer.collaborator:
        customer_seller_email = f"{customer.collaborator.email}"
    else:
        customer_seller_email = "None"

    customer_summary = f"{customer_id}, {customer_firstname}, {customer_lastname}, {customer_email}, {customer_phone}, {customer_company}, {customer_seller_email}"

    return customer_summary


def display_list_customer(customers):
    table = Table(title="[bold yellow]Customers List:[/bold yellow]")

    table.add_column("ID")
    table.add_column("Firstname")
    table.add_column("Lastname")
    table.add_column("Email")
    table.add_column("Phone")
    table.add_column("Company")
    table.add_column("Seller Email")

    for customer in customers:
        formatted_customer = display_customer_summary(customer)
        table.add_row(*formatted_customer.split(", "))

    console.print(table)
