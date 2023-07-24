import click

from .auth_controllers.log_cli import login, logout, login_form, logout_form
from .user_controllers.collaborator_controllers.collaborator_cli import collaborator, collaborator_form
from .business_controllers.customer_controllers.customer_cli import customer, customer_form
from .business_controllers.contract_controllers.contract_cli import contract, contract_form
from .business_controllers.event_controllers.event_cli import event, event_form


@click.group()
@click.pass_context
def form(ctx):
    pass


form.add_command(login_form, name='login')
form.add_command(logout_form, name='logout')
form.add_command(collaborator_form, name='collaborator')
form.add_command(customer_form, name='customer')
form.add_command(contract_form, name='contract')
form.add_command(event_form, name='event')


@click.group()
@click.pass_context
def cli(ctx):
    pass


cli.add_command(form, name='form')
cli.add_command(login, name='login')
cli.add_command(logout, name='logout')
cli.add_command(collaborator, name='collaborator')
cli.add_command(customer, name='customer')
cli.add_command(contract, name='contract')
cli.add_command(event, name='event')
