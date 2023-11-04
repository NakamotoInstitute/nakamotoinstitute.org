import click
from flask import Blueprint

from sni.cli.utils import DONE, color_text
from sni.content.update import update_content
from sni.utils.db import flush_db

blueprint = Blueprint("content", __name__)

blueprint.cli.help = "Manage content."


@blueprint.cli.command()
def initialize():
    """Initialize and seed database."""
    click.echo("Initializing database...", nl=False)
    flush_db()
    click.echo(DONE)
    update_content()
    click.echo(color_text("Finished importing data!"))
