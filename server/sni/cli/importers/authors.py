import click

from sni.authors.models import Author
from sni.authors.schemas.base import AuthorMDModel
from sni.cli.utils import DONE, load_all_markdown_files
from sni.extensions import db


def import_author():
    click.echo("Importing Author...", nl=False)
    authors_data = load_all_markdown_files("content/authors", AuthorMDModel)
    for author_data in authors_data:
        author = Author(**author_data)
        db.session.add(author)
    db.session.commit()
    click.echo(DONE)
