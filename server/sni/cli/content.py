import click
from flask import Blueprint

from sni.cli.utils import color_text
from sni.content.update import update_content

blueprint = Blueprint("content", __name__)

blueprint.cli.help = "Manage content."


@blueprint.cli.command()
def initialize():
    """Initialize and seed database."""
    click.echo("Initializing database...", nl=False)
    update_content()
    click.echo(color_text("Finished importing data!"))
