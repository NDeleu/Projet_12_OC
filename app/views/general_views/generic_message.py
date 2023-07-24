from rich.console import Console

console = Console()


def display_message(message):
    console.print(f"[green]{message}[/green]")


def display_message_success(message):
    console.print(f"[bold green]{message}[/bold green]")


def display_message_error(message):
    console.print(f"[bold red]{message}[/bold red]")


def display_message_info(message):
    console.print(f"[bold blue]{message}[/bold blue]")
