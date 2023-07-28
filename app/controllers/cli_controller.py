import click

from .auth_controllers.log_cli import login, logout, loginform, logoutform
from .user_controllers.collaborator_controllers.collaborator_cli import collaborator, collaboratorform
from .business_controllers.customer_controllers.customer_cli import customer, customerform
from .business_controllers.contract_controllers.contract_cli import contract, contractform
from .business_controllers.event_controllers.event_cli import event, eventform
from .utils_controllers.generate_uml_cli import generateuml


@click.group(help="A variety of application-related utility tools")
@click.pass_context
def utils(ctx):
    pass


utils.add_command(generateuml, name="generateuml")


@click.group(help="Various forms for login, logout, etc.")
@click.pass_context
def form(ctx):
    pass


form.add_command(loginform, name='login')
form.add_command(logoutform, name='logout')
form.add_command(collaboratorform, name='collaborator')
form.add_command(customerform, name='customer')
form.add_command(contractform, name='contract')
form.add_command(eventform, name='event')


@click.group(help="Main command group")
@click.pass_context
def cli(ctx):
    pass


cli.add_command(utils, name='utils')
cli.add_command(form, name='form')
cli.add_command(login, name='login')
cli.add_command(logout, name='logout')
cli.add_command(collaborator, name='collaborator')
cli.add_command(customer, name='customer')
cli.add_command(contract, name='contract')
cli.add_command(event, name='event')
