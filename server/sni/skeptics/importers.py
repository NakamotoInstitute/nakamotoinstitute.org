from sni.content.json import import_json_data
from sni.models import Skeptic
from sni.skeptics.schemas import SkepticsJSONModel


def import_skeptics(db_session, force: bool = False, force_conditions: list[bool] = []):
    return import_json_data(
        db_session,
        model=Skeptic,
        schema=SkepticsJSONModel,
        file_path="data/skeptics.json",
        force=force or any(force_conditions),
    )
