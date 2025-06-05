from sni.content.markdown import create_basic_importer
from sni.database import SessionLocalSync
from sni.models import Translator

from .schemas import TranslatorMDModel


def import_translators(directory: str, force: bool = False):
    with SessionLocalSync() as session:
        importer = create_basic_importer(
            directory=directory,
            session=session,
            canonical_model=Translator,
            schema=TranslatorMDModel,
            force=force,
        )
        importer.run()
