from rich.console import Console

console = Console()


def display_customer(customer):
    console.print("[bold green]Administrator found:[/bold green]")
    console.print(f"ID: {customer.id}")
    console.print(f"firstname: {customer.firstname}")
    console.print(f"Lastname: {customer.lastname}")
    console.print(f"Email: {customer.email}")
    console.print(f"Phone: {customer.phone}")
    console.print(f"Company: {customer.company}")
    console.print(f"Creation Date: {customer.date_created}")
    console.print(f"Update Date: {customer.date_updated}")
    console.print(f"Seller contact: {customer.collaborator.firstname} {customer.collaborator.lastname}")
