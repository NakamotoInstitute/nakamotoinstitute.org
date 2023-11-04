from sni.content.importers import JSONImporter
from sni.skeptics.models import Skeptic, SkepticFile
from sni.skeptics.schemas import SkepticJSONModel


class SkepticImporter(JSONImporter):
    filepath = "data/skeptics.json"
    item_schema = SkepticJSONModel
    model = Skeptic
    file_model = SkepticFile
    content_type = "skeptics"
    query_field = "slug"
