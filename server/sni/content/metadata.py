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


def needs_update(force: bool, file_metadata: FileMetadata, current_hash: str) -> bool:
    return force or file_metadata.hash != current_hash


def get_hash(filepath: str) -> str:
    return (
        get_directory_hash(filepath)
        if os.path.isdir(filepath)
        else get_file_hash(filepath)
    )


def process_metadata(
    db_session: Session,
    filepath: str,
    existing_metadata: FileMetadata | None,
    force: bool = False,
) -> tuple[Actions, FileMetadata | None]:
    current_hash = get_hash(filepath)
    current_timestamp = datetime.fromtimestamp(os.path.getmtime(filepath))

    action = Actions.UNCHANGED
    metadata = existing_metadata

    if not existing_metadata:
        metadata = FileMetadata(
            filename=filepath, hash=current_hash, last_modified=current_timestamp
        )
        action = Actions.NEW
    elif needs_update(force, existing_metadata, current_hash):
        metadata.hash = current_hash
        metadata.last_modified = current_timestamp
        action = Actions.UPDATED

    if action != Actions.UNCHANGED:
        db_session.add(metadata)
        db_session.flush()

    return action, metadata


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
