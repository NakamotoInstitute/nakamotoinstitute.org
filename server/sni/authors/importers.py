from sni.content.markdown import create_basic_importer
from sni.database import SessionLocalSync
from sni.models import Author

from .schemas.base import AuthorMDModel


def import_authors(directory: str, force: bool = False):
    with SessionLocalSync() as session:
        importer = create_basic_importer(
            directory=directory,
            session=session,
            canonical_model=Author,
            schema=AuthorMDModel,
            force=force,
        )
        importer.run()
