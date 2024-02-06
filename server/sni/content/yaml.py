from datetime import datetime
from typing import Any, Dict, List, Type

import yaml
from pydantic import BaseModel, Field, ValidationError
from sqlalchemy import select
from sqlalchemy.orm import Session

from sni.database import Base
from sni.models import FileMetadata
from sni.utils.files import get_file_hash


class SlugWeight(BaseModel):
    slug: str
    weight: int = Field(ge=0)


class SlugWeights(BaseModel):
    weights: List[SlugWeight]


class WeightImporter:
    file_updated = False
    schema = SlugWeights

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def load_yaml_data(
        self, file_path: str, force: bool = False
    ) -> List[Dict[str, Any]]:
        self.handle_file_metadata(file_path, force)
        try:
            with open(file_path, "r") as file:
                return yaml.safe_load(file)
        except Exception as e:
            print(f"Error loading YAML data: {e}")
            return []

    def handle_file_metadata(self, file_path: str, force: bool = False):
        existing_metadata = self.db_session.scalars(
            select(FileMetadata).filter_by(filename=file_path)
        ).first()

        current_hash = get_file_hash(file_path)
        current_last_modified = datetime.now()

        if existing_metadata:
            if existing_metadata.hash != current_hash or force:
                existing_metadata.hash = current_hash
                existing_metadata.last_modified = current_last_modified
                self.file_updated = True
            self.file_metadata = existing_metadata
        else:
            self.file_metadata = FileMetadata(
                filename=file_path,
                hash=current_hash,
                last_modified=current_last_modified,
            )
            self.db_session.add(self.file_metadata)

            new_file = self.file_model(
                file_metadata=self.file_metadata, content_type=self.content_type
            )

            self.db_session.add(new_file)
            self.db_session.flush()
            self.file_updated = True

        self.yaml_file = self.file_metadata.yaml_file

    def process_item_data(self, item_data: Dict) -> Dict:
        return item_data

    def process_data(self, items: List[Base], slug_weights: Dict[str, int]):
        for item in items:
            weight = slug_weights.get(item.slug, 0)
            if self.parent:
                parent = getattr(item, self.parent)
                parent.weight = weight
                self.db_session.add(parent)
            else:
                item.weight = weight
                self.db_session.add(item)

    def validate_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if not self.schema:
            raise ValueError("Pydantic schema not defined in subclass")

        try:
            return self.schema(**data).dict()
        except ValidationError as e:
            print(f"Validation error: {e}")
            raise

    def commit_changes(self):
        try:
            self.db_session.commit()
        except Exception as e:
            print(f"Error committing changes to the database: {e}")
            self.db_session.rollback()

    def import_data(self, force: bool = False):
        print(f"Importing weights for {self.model.__name__}...", end="")
        yaml_data = self.load_yaml_data(self.file_path, force)
        if self.file_updated or force:
            self.items = self.db_session.scalars(select(self.model)).unique().all()
            validated_data = self.validate_data(yaml_data)
            slug_weights = {
                item["slug"]: item["weight"] for item in validated_data["weights"]
            }
            self.process_data(self.items, slug_weights)
            self.commit_changes()
        print("DONE")


def run_weight_importer(
    importer_cls: Type[WeightImporter],
    db_session: Session,
    force: bool = False,
    force_conditions: List[bool] = [],
) -> bool:
    importer = importer_cls(db_session)
    importer.import_data(force or any(force_conditions))
    return importer.file_updated
