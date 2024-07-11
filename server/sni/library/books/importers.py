from sni.content.markdown import MarkdownDirectoryImporter

from .schemas import BookMDModel, BookMDNodeModel


class LibraryBookImporter(MarkdownDirectoryImporter):
    directory_path = "content/library"
    content_type = "Library Books"
    manifest_schema = BookMDModel
    node_schema = BookMDNodeModel
    content_key = "document"
