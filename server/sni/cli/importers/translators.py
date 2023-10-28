from sni.cli.utils import ContentImporter
from sni.translators.models import Translator
from sni.translators.schemas import TranslatorMDModel


class TranslatorImporter(ContentImporter):
    content_type = "Translator"
    model = Translator
    schema = TranslatorMDModel
    content_key = "translator"


def import_translator():
    translator_importer = TranslatorImporter(directory_path="content/translators")
    translator_importer.run_import()
