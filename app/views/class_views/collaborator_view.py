from rich.console import Console

console = Console()


def display_collaborator(collaborator):
    console.print("[bold yellow]Administrator found:[/bold yellow]")
    console.print(f"ID: {collaborator.id}")
    console.print(f"Firstname: {collaborator.firstname}")
    console.print(f"Lastname: {collaborator.lastname}")
    console.print(f"Role: {collaborator.role}")
    console.print(f"Email: {collaborator.email}")
