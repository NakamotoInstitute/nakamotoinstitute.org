import click

from app.cli.utils import DONE, import_content
from app.library.schemas import LibraryMDSchema, LibraryTranslatedMDSchema
from app.models import Document, DocumentTranslation


def import_library():
    click.echo("Importing Library...", nl=False)
    import_content(
        "content/library",
        LibraryMDSchema,
        LibraryTranslatedMDSchema,
        Document,
        DocumentTranslation,
        ["title", "sort_title", "image_alt"],
        "document",
    )
    click.echo(DONE)
