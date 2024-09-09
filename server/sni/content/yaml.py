from typing import Type

import yaml
from pydantic import BaseModel, Field, ValidationError
from sqlalchemy import select, update
from sqlalchemy.orm import Session

from sni.content.metadata import Actions, process_metadata
from sni.database import Base
from sni.models import FileMetadata, YAMLContent
from sni.shared.schemas import IterableRootModel


class SlugWeight(BaseModel):
    slug: str
    weight: int = Field(ge=0)


class SlugWeights(IterableRootModel):
    root: list[SlugWeight]


def import_yaml_weights(
    db_session: Session,
    model: Type[Base],
    file_path: str,
    force: bool = False,
) -> bool:
    print(f"Importing weights for {model.__name__}...", end="")

    action, metadata = process_metadata(
        db_session,
        file_path,
        db_session.scalars(select(FileMetadata).filter_by(filename=file_path)).first(),
        force,
    )

    if action == Actions.UNCHANGED:
        print("DONE")
        return False

    try:
        with open(file_path, "r") as file:
            raw_content = file.read()
            yaml_data = yaml.safe_load(raw_content)
        validated_data = SlugWeights.model_validate(yaml_data)
    except ValidationError as e:
        print(f"\nValidation error: {e}")
        return False
    except Exception as e:
        print(f"\nError loading YAML: {e}")
        return False

    try:
        if action == Actions.NEW:
            content = YAMLContent(file_metadata=metadata, file_content=raw_content)
            db_session.add(content)
            db_session.flush()

        db_session.execute(
            update(model),
            [
                {
                    "id": item.id,
                    "weight": next(
                        (
                            data.weight
                            for data in validated_data.root
                            if data.slug == item.slug
                        ),
                        0,
                    ),
                }
                for item in db_session.scalars(select(model)).unique()
            ],
        )

        db_session.commit()
        print("DONE")
        return True

    except Exception as e:
        print(f"\nDatabase error: {e}")
        db_session.rollback()
        return False
