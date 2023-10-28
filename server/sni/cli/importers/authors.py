from sni.authors.models import Author
from sni.authors.schemas.base import AuthorMDModel
from sni.cli.utils import ContentImporter


class AuthorImporter(ContentImporter):
    content_type = "Author"
    model = Author
    schema = AuthorMDModel
    content_key = "author"


def import_author():
    author_importer = AuthorImporter(directory_path="content/authors")
    author_importer.run_import()
