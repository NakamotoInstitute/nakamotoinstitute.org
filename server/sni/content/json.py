import json
from datetime import datetime
from typing import Any, Dict, List, Type

from pydantic import BaseModel, ValidationError
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from sni.models import FileMetadata
from sni.utils.files import get_file_hash


class JSONImporter:
    schema: Type[BaseModel]
    dependent_importers: List[Type["JSONImporter"]] = []
    existing_thread_ids = set()
    file_updated = False

    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.fetch_existing_item_ids()

    def fetch_existing_item_ids(self):
        result = self.db_session.scalars(select(self.model.id)).all()
        self.existing_item_ids = set(result)

    def load_json_data(
        self, file_path: str, force: bool = False
    ) -> List[Dict[str, Any]]:
        self.handle_file_metadata(file_path, force)
        try:
            with open(file_path, "r") as file:
                return json.load(file)
        except Exception as e:
            print(f"Error loading JSON data: {e}")
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

        self.json_file = self.file_metadata.json_file

        if self.file_updated:
            self.delete_all_existing_items()

    def delete_dependent_entities(self):
        for dependent_importer_cls in self.dependent_importers:
            dependent_importer = dependent_importer_cls(self.db_session)
            dependent_importer.delete_all_existing_items()

    def delete_all_existing_items(self):
        self.delete_dependent_entities()
        self.db_session.execute(delete(self.model))

    def validate_data(self, data: list[dict[str, Any]]) -> Dict[str, Any]:
        if not self.schema:
            raise ValueError("Pydantic schema not defined in subclass")

        try:
            return self.schema.model_validate(data).dict()
        except ValidationError as e:
            print(f"Validation error: {e}")
            raise

    def process_item_data(self, item_data: Dict) -> Dict:
        return item_data

    def process_data(self, validated_data: List[Dict[str, Any]]):
        for item_data in validated_data:
            new_item = self.model(
                **self.process_item_data(item_data), file_id=self.json_file.id
            )
            self.db_session.add(new_item)

    def commit_changes(self):
        try:
            self.db_session.commit()
        except Exception as e:
            print(f"Error committing changes to the database: {e}")
            self.db_session.rollback()

    def import_data(self, force: bool = False):
        print(f"Importing {self.model.__name__}...", end="")
        json_data = self.load_json_data(self.file_path, force)
        if self.file_updated or force:
            validated_data = self.validate_data(json_data)
            self.process_data(validated_data)
            self.commit_changes()
        print("DONE")


def run_json_importer(
    importer_cls: Type[JSONImporter],
    db_session: Session,
    force: bool = False,
    force_conditions: List[bool] = [],
) -> bool:
    importer = importer_cls(db_session)
    importer.import_data(force or any(force_conditions))
    return importer.file_updated
