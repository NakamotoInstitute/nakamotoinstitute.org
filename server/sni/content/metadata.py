import collections
import os
from datetime import datetime
from enum import Enum

from sqlalchemy.orm import Session

from sni.models import FileMetadata
from sni.utils.files import get_directory_hash, get_file_hash


class Actions(Enum):
    NEW = "new"
    UPDATED = "updated"
    UNCHANGED = "unchanged"
    DELETED = "deleted"


def get_hash(filepath: str) -> str:
    return (
        get_directory_hash(filepath)
        if os.path.isdir(filepath)
        else get_file_hash(filepath)
    )


def create_metadata_for_new_file(filepath: str) -> FileMetadata:
    current_hash = get_hash(filepath)
    current_timestamp = datetime.fromtimestamp(os.path.getmtime(filepath))
    return FileMetadata(
        filename=filepath,
        hash=current_hash,
        last_modified=current_timestamp,
    )


def update_metadata_if_needed(
    filepath: str, existing_metadata: FileMetadata, force=False
) -> tuple[Actions, FileMetadata]:
    current_hash = get_hash(filepath)
    if not force and existing_metadata.hash == current_hash:
        return Actions.UNCHANGED, existing_metadata

    current_timestamp = datetime.fromtimestamp(os.path.getmtime(filepath))
    existing_metadata.hash = current_hash
    existing_metadata.last_modified = current_timestamp
    return Actions.UPDATED, existing_metadata


def process_metadata(
    db_session, filepath: str, existing_metadata: FileMetadata | None, force=False
) -> tuple[Actions, FileMetadata]:
    if not existing_metadata:
        metadata = create_metadata_for_new_file(filepath)
        db_session.add(metadata)
        db_session.flush()
        return Actions.NEW, metadata
    else:
        action, updated_metadata = update_metadata_if_needed(
            filepath, existing_metadata, force
        )
        if action != Actions.UNCHANGED:
            db_session.add(updated_metadata)
            db_session.flush()
        return action, updated_metadata


class MetadataManager:
    def __init__(self, db_session: Session, force: bool = False):
        self.db_session = db_session
        self.force = force
        self.actions = collections.Counter({action: 0 for action in Actions})

    def record_action(self, action: Actions):
        self.actions[action] += 1

    def get_action_summary(self) -> str:
        return (
            f"{self.actions[Actions.NEW]} new, "
            f"{self.actions[Actions.UPDATED]} updated, "
            f"{self.actions[Actions.DELETED]} deleted\n"
        )

    def process_file(
        self, filepath: str, existing_metadata: FileMetadata | None
    ) -> tuple[Actions, FileMetadata | None]:
        return process_metadata(
            self.db_session, filepath, existing_metadata, self.force
        )

    def create_metadata(self, filepath: str) -> FileMetadata:
        metadata = create_metadata_for_new_file(filepath)
        self.db_session.add(metadata)
        self.db_session.flush()
        self.record_action(Actions.NEW)
        return metadata

    def update_metadata(
        self, filepath: str, existing_metadata: FileMetadata
    ) -> tuple[Actions, FileMetadata]:
        action, updated_metadata = update_metadata_if_needed(
            filepath, existing_metadata, self.force
        )
        if action != Actions.UNCHANGED:
            self.db_session.add(updated_metadata)
            self.db_session.flush()
            self.record_action(action)
        return action, updated_metadata
