import json
from typing import Callable, Type

from pydantic import BaseModel
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from sni.database import Base
from sni.models.content import FileMetadata, JSONContent

from .metadata import Actions, process_metadata


def import_json_data(
    db_session: Session,
    model: Type[Base],
    schema: Type[BaseModel],
    file_path: str,
    force: bool = False,
    process_item: Callable[[dict], dict] = lambda x: x,
    dependent_models: list[Type[Base]] = [],
):
    print(f"Importing {model.__name__}...", end="")
    existing_metadata = db_session.scalars(
        select(FileMetadata).filter_by(filename=file_path)
    ).first()

    action, metadata = process_metadata(db_session, file_path, existing_metadata, force)

    if action != Actions.UNCHANGED or force:
        with open(file_path) as f:
            data = json.load(f)

        if action == Actions.NEW:
            content = JSONContent(file_metadata=metadata, file_content=json.dumps(data))
            db_session.add(content)
            db_session.flush()

        validated_data = schema.model_validate(data).model_dump()

        # Delete dependent data
        for dep_model in dependent_models:
            db_session.execute(delete(dep_model))
        db_session.execute(delete(model))

        # Insert new data
        db_session.add_all(
            [
                model(**process_item(item), content_id=metadata.content.id)
                for item in validated_data
            ]
        )

    db_session.commit()
    print("DONE")
    return action != Actions.UNCHANGED
