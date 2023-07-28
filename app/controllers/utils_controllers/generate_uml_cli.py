import click

from app.models import generate_uml_graph


@click.command(help="Generate - or update if already existing - the erd uml graph")
@click.pass_context
def generateuml(ctx):
    generate_uml_graph()
