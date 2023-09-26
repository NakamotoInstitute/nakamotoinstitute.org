import click

from app import db
from app.authors.schemas import AuthorMDSchema
from app.cli.utils import DONE, load_all_markdown_files
from app.models import Author


def import_author():
    click.echo("Importing Author...", nl=False)
    authors_data = load_all_markdown_files("content/authors", AuthorMDSchema)
    for author_data in authors_data:
        author = Author(**author_data)
        db.session.add(author)
    db.session.commit()
    click.echo(DONE)
