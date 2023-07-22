from rich.console import Console

console = Console()


def display_collaborator(collaborator):
    console.print("[bold green]Administrator found:[/bold green]")
    console.print(f"ID: {collaborator.id}")
    console.print(f"Surname: {collaborator.surname}")
    console.print(f"Lastname: {collaborator.lastname}")
    console.print(f"Role: {collaborator.role}")
    console.print(f"Email: {collaborator.email}")
