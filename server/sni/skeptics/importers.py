from sni.content.json import JSONImporter
from sni.models import Skeptic, SkepticFile
from sni.skeptics.schemas import SkepticsJSONModel


class SkepticImporter(JSONImporter):
    file_path = "data/skeptics.json"
    schema = SkepticsJSONModel
    model = Skeptic
    file_model = SkepticFile
    content_type = "skeptics"
