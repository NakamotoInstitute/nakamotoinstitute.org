import click

from sni.extensions import db
from sni.authors.schemas import AuthorMDModel
from sni.cli.utils import DONE, load_all_markdown_files
from sni.models import Author


def import_author():
    click.echo("Importing Author...", nl=False)
    authors_data = load_all_markdown_files("content/authors", AuthorMDModel)
    for author_data in authors_data:
        author = Author(**author_data)
        db.session.add(author)
    db.session.commit()
    click.echo(DONE)
