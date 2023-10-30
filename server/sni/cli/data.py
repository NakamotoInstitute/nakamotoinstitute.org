import click
from flask import Blueprint

from sni.cli.importers import (
    import_author,
    import_email,
    import_email_thread,
    import_episode,
    import_forum_post,
    import_forum_thread,
    import_library,
    import_mempool,
    import_mempool_series,
    import_quote,
    import_quote_category,
    import_skeptic,
    import_translator,
)
from sni.cli.utils import color_text, flush_db

blueprint = Blueprint("data", __name__)

blueprint.cli.help = "Update database."


def seed_db():
    import_author()
    import_translator()
    import_email()
    import_email_thread()
    import_forum_post()
    import_forum_thread()
    import_quote_category()
    import_quote()
    import_library()
    import_mempool_series()
    import_mempool()
    import_skeptic()
    import_episode()


@blueprint.cli.command()
def seed():
    """Initialize and seed database."""
    flush_db()
    seed_db()
    click.echo(color_text("Finished importing data!"))
