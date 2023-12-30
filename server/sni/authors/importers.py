from sni.content.markdown import MarkdownImporter
from sni.models import Author

from .schemas.base import AuthorMDModel


class AuthorImporter(MarkdownImporter):
    directory_path = "content/authors"
    content_type = "Author"
    model = Author
    schema = AuthorMDModel
    content_key = "author"
