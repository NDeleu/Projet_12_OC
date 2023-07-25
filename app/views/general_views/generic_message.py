from rich.console import Console

console = Console()


def display_message_success(message):
    console.print(f"[bold green]SUCCESS: {message}[/bold green]")


def display_message_error(message):
    console.print(f"[bold red]ERROR: {message}[/bold red]")


def display_message_info(message):
    console.print(f"[bold blue]{message}[/bold blue]")


def display_message_correction(message):
    console.print(f"[bold orange]CARE: {message}[/bold orange]")