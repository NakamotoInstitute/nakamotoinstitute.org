import json
import os
from datetime import datetime

import click
from pydantic import BaseModel, ValidationError

from sni.cli.utils import DONE
from sni.extensions import db
from sni.shared.models import FileMetadata
from sni.utils.files import get_file_hash


def load_and_validate_json(
    json_file: str,
    item_schema: BaseModel,
):
    try:
        with open(json_file, "r") as file:
            data = json.load(file)
            if not isinstance(data, list):
                print(
                    f"Invalid data format. Expected a list but got {type(data).__name__}"  # noqa: E501
                )
                return None

            validated_data = [item_schema(**item) for item in data]
            return validated_data
    except ValidationError as e:
        print(f"Validation error: {e}")
        return None
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return None


class JSONImporter:
    query_field = "id"

    def load_and_validate_json(self):
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
                if not isinstance(data, list):
                    print(
                        f"Invalid data format. Expected a list but got {type(data).__name__}"  # noqa: E501
                    )
                    return None

                validated_data = [self.item_schema(**item) for item in data]
                return validated_data
        except ValidationError as e:
            print(f"Validation error: {e}")
            return None
        except Exception as e:
            print(f"Error loading JSON file: {e}")
            return None

    def create_metadata_and_items(self, items_data, current_hash, current_timestamp):
        new_metadata = FileMetadata(
            filename=self.filepath, hash=current_hash, last_modified=current_timestamp
        )
        db.session.add(new_metadata)

        file_obj = self.file_model(
            file_metadata=new_metadata, content_type=self.content_type
        )

        for item_data in items_data:
            item = self.model(**item_data.dict(), file=file_obj)
            db.session.add(item)

    def update_metadata_and_items(
        self, file_metadata, items_data, current_hash, current_timestamp
    ):
        if (
            file_metadata.last_modified != current_timestamp
            or file_metadata.hash != current_hash
        ):
            for item_data in items_data:
                try:
                    item = db.session.scalars(
                        db.select(self.model).filter_by(
                            {self.query_field: item_data[self.query_field]}
                        )
                    ).first()
                    if item:
                        for key, value in item_data.items():
                            setattr(item, key, value)
                    else:
                        item = self.model(**item_data, file_id=file_metadata.id)
                        db.session.session.add(item)
                except KeyError:
                    raise KeyError(f"Item missing '{self.query_field}': {item_data}")

            file_metadata.last_modified = current_timestamp
            file_metadata.hash = current_hash

    def run_import(self):
        click.echo(f"Importing {self.model.__name__}...", nl=False)
        items_data = self.load_and_validate_json()

        if not items_data:
            return

        current_hash = get_file_hash(self.filepath)
        current_timestamp = datetime.fromtimestamp(os.path.getmtime(self.filepath))

        file_metadata = db.session.scalars(
            db.select(FileMetadata).filter_by(filename=self.filepath).limit(1)
        ).first()

        if not file_metadata:
            self.create_metadata_and_items(items_data, current_hash, current_timestamp)
        else:
            self.update_metadata_and_items(
                file_metadata, items_data, current_hash, current_timestamp
            )

        db.session.commit()
        click.echo(DONE)
