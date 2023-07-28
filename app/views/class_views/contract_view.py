from rich.console import Console
from rich.table import Table

console = Console()


def display_contract_detail(contract):
    console.print("[bold yellow]Contract Details:[/bold yellow]")
    console.print(f"Contract ID: {contract.id}")
    console.print(f"Total Amount: {contract.total_amount}")
    console.print(f"Left to Pay: {contract.left_to_pay}")
    console.print(f"Date Created: {contract.date_created}")
    console.print(f"Signed: {'Yes' if contract.signed else 'No'}")
    if contract.customer:
        console.print("Customer:")
        console.print(f"  Customer ID: {contract.customer_id}")
        console.print(f"  Customer Name: {contract.customer.firstname} - {contract.customer.lastname}")
        console.print(f"  Customer Email: {contract.customer.email}")
    else:
        console.print("Customer: None")
    if contract.customer.collaborator:
        console.print("Seller assigned:")
        console.print(f"  Seller ID assigned: {contract.customer.collaborator_id}")
        console.print(f"  Seller Name assigned: {contract.customer.collaborator.firstname} - {contract.customer.collaborator.lastname}")
        console.print(f"  Seller Email assigned: {contract.customer.collaborator.email}")
    else:
        console.print("Seller assigned: None")
    if contract.event:
        console.print("Event:")
        console.print(f"  Event ID: {contract.event.id}")
        console.print(f"  Event Name: {contract.event.name}")
        console.print(f"  Event Start Time: {contract.event.event_start}")
        console.print(f"  Event End Time: {contract.event.event_end}")
    else:
        console.print("Event: None")


def display_contract_summary(contract):
    contract_id = f"{contract.id}"
    contract_total_amount = f"{contract.total_amount}"
    contract_left_to_pay = f"{contract.left_to_pay}"
    contract_date_created = f"{contract.date_created}"
    contract_signed = f"{'Yes' if contract.signed else 'No'}"

    contract_summary = f"{contract_id}, {contract_total_amount}, {contract_left_to_pay}, {contract_date_created}, {contract_signed}"

    return contract_summary


def display_list_contracts(contracts):
    table = Table(title="[bold yellow]Contracts List:[/bold yellow]")

    table.add_column("ID")
    table.add_column("Total Amount")
    table.add_column("Left to Pay")
    table.add_column("Date Created")
    table.add_column("Signed")

    for contract in contracts:
        formatted_contract = display_contract_summary(contract)
        table.add_row(*formatted_contract.split(", "))

    console.print(table)
