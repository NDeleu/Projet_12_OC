from rich.console import Console

console = Console()


def display_contract(contract):
    console.print("[bold green]Contract Details:[/bold green]")
    console.print(f"Contract ID: {contract.id}")
    console.print(f"Date Created: {contract.date_created}")
    console.print(f"Total Amount: {contract.total_amount}")
    console.print(f"Left to Pay: {contract.left_to_pay}")
    console.print(f"Signed: {'Yes' if contract.signed else 'No'}")
    console.print(f"Customer ID: {contract.customer_id}")
    if contract.event:
        console.print("Event:")
        console.print(f"  Event ID: {contract.event.id}")
        console.print(f"  Event Name: {contract.event.name}")
        console.print(f"  Event Start Time: {contract.event.event_start}")
        console.print(f"  Event End Time: {contract.event.event_end}")
    else:
        console.print("Event: None")
