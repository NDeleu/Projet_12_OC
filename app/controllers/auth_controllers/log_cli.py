import click
from .log_controller import login_func, logout_func
from app.views.general_views.generic_message import display_message_info
from app.views.general_views.generic_message import display_message_error


@click.command(help="Login with form")
@click.pass_context
def login_form(ctx):
    try:
        session = ctx.obj
        display_message_info("Enter your email")
        email = click.prompt("Email", type=click.STRING)
        display_message_info("Enter your password")
        password = click.prompt("Password", type=click.STRING, hide_input=True)
        login_func(session, email, password)
    except Exception as e:
        display_message_error(str(e))


@click.command(help="Logout the user")
@click.pass_context
def logout_form(ctx):
    try:
        session = ctx.obj
        user = None
        logout_func(session, user)
    except Exception as e:
        display_message_error(str(e))


@click.command(help="Login")
@click.pass_context
@click.argument('email', type=str, help="Enter your email")
@click.argument('password', type=str, help="Enter your password")
def login(ctx, email, password):
    try:
        session = ctx.obj
        login_func(session, email, password)
    except Exception as e:
        display_message_error(str(e))


@click.command(help="Logout the user")
@click.pass_context
def logout(ctx):
    try:
        session = ctx.obj
        user = None
        logout_func(session, user)
    except Exception as e:
        display_message_error(str(e))
