from sni.content.json import JSONImporter
from sni.models import Skeptic, SkepticFile
from sni.skeptics.schemas import SkepticJSONModel


class SkepticImporter(JSONImporter):
    file_path = "data/skeptics.json"
    schema = SkepticJSONModel
    model = Skeptic
    file_model = SkepticFile
    content_type = "skeptics"
