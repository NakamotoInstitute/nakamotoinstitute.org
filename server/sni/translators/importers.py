from sni.content.importers import MarkdownImporter
from sni.models import Translator

from .schemas import TranslatorMDModel


class TranslatorImporter(MarkdownImporter):
    directory_path = "content/translators"
    content_type = "Translator"
    model = Translator
    schema = TranslatorMDModel
    content_key = "translator"
