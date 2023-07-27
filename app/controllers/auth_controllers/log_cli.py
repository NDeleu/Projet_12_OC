import click
from .log_controller import login_func, logout_func
from app.views.general_views.generic_message import display_message_info
from app.views.general_views.generic_message import display_message_error


@click.command(help="Login with form")
@click.pass_context
def loginform(ctx):
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
def logoutform(ctx):
    try:
        session = ctx.obj
        logout_func(session)
    except Exception as e:
        display_message_error(str(e))


@click.command(help="Login\n\n"
                    "Parameters:\n"
                    "   email (str): Enter your email\n"
                    "   password (str): Enter your password")
@click.pass_context
@click.argument('email', type=str)
@click.argument('password', type=str)
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
        logout_func(session)
    except Exception as e:
        display_message_error(str(e))
