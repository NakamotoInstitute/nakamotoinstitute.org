from sni.authors.models import Author
from sni.authors.schemas.base import AuthorMDModel
from sni.content.importers import MarkdownImporter


class AuthorImporter(MarkdownImporter):
    directory_path = "content/authors"
    content_type = "Author"
    model = Author
    schema = AuthorMDModel
    content_key = "author"


def import_author():
    author_importer = AuthorImporter()
    author_importer.run_import()
