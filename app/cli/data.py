import click
from flask import Blueprint

from app.cli.importers import (
    import_author,
    import_library,
    import_mempool,
    import_translator,
)
from app.cli.utils import color_text, flush_db

bp = Blueprint("data", __name__)

bp.cli.help = "Update database."


@bp.cli.command()
def seed():
    """Initialize and seed database."""
    flush_db()
    import_author()
    import_translator()
    import_library()
    import_mempool()
    click.echo(color_text("Finished importing data!"))
