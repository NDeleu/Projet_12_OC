import click
from .log_controller import login_func, logout_func


@click.command()
@click.pass_context
def login_form(ctx):
    session = ctx.obj
    email = click.prompt("Email", type=click.STRING)
    password = click.prompt("Password", type=click.STRING, hide_input=True)
    login_func(session, email, password)


@click.command()
@click.pass_context
def logout_form(ctx):
    session = ctx.obj
    user = None
    logout_func(session, user)


@click.command()
@click.pass_context
@click.argument('email', type=str)
@click.argument('password', type=str)
def login(ctx, email, password):
    session = ctx.obj
    login_func(session, email, password)


@click.command()
@click.pass_context
def logout(ctx):
    session = ctx.obj
    user = None
    logout_func(session, user)
