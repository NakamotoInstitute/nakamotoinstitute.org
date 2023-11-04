from sni.content.importers import MarkdownImporter
from sni.translators.models import Translator
from sni.translators.schemas import TranslatorMDModel


class TranslatorImporter(MarkdownImporter):
    directory_path = "content/translators"
    content_type = "Translator"
    model = Translator
    schema = TranslatorMDModel
    content_key = "translator"
