from ..metadata import MetadataManager
from .differs import diff_states
from .handlers import BasicHandler, ManifestBasedTranslatedHandler, TranslatedHandler
from .loaders import (
    load_basic_db_state,
    load_basic_fs_state,
    load_manifest_based_db_state,
    load_manifest_based_fs_state,
    load_translated_db_state,
    load_translated_fs_state,
)


class Importer:
    def __init__(
        self, directory, session, fs_loader, db_loader, handler, metadata_manager
    ):
        self.directory = directory
        self.session = session
        self.fs_loader = fs_loader
        self.db_loader = db_loader
        self.handler = handler
        self.metadata_manager = metadata_manager

    def run(self):
        print(f"Starting {self.handler.canonical_model.__name__} import...", end="")
        try:
            fs_state = self.fs_loader(self.directory)
            db_state = self.db_loader()

            new, deleted, existing = diff_states(fs_state, db_state)

            for item in new:
                self.handler.handle_new(item, fs_state[item])

            for item in deleted:
                self.handler.handle_deleted(db_state[item])

            for item in existing:
                self.handler.handle_existing(item, fs_state[item], db_state[item])

            self.session.commit()
        finally:
            self.session.close()
        print("DONE")
        print(self.metadata_manager.get_action_summary())


def create_basic_importer(
    directory,
    session,
    canonical_model,
    schema,
    handler_class=BasicHandler,
    force=False,
    **handler_kwargs,
):
    metadata_manager = MetadataManager(session, force=force)
    import_handler = handler_class(
        session=session,
        metadata_manager=metadata_manager,
        schema=schema,
        canonical_model=canonical_model,
        **handler_kwargs,
    )
    return Importer(
        directory=directory,
        session=session,
        fs_loader=load_basic_fs_state,
        db_loader=lambda: load_basic_db_state(session, canonical_model),
        handler=import_handler,
        metadata_manager=metadata_manager,
    )


def create_translated_importer(
    directory,
    session,
    canonical_model,
    translation_model,
    schemas,
    content_key,
    handler_class=TranslatedHandler,
    force=False,
    **handler_kwargs,
):
    """
    Factory function for creating a TranslatedImporter.

    Args:
        directory (str): Filesystem path to import from.
        session (Session): SQLAlchemy session.
        canonical_model: ORM model for canonical content.
        translation_model: ORM model for translations.
        schemas (dict): Schemas for file processing.
        content_key (str): Attribute name for the canonical back-reference in translations.
        handler_class: Handler class to use (default: TranslatedHandler).
        force (bool): Force metadata update.
        **handler_kwargs: Extra arguments for the handler.
    """  # noqa: E501
    metadata_manager = MetadataManager(session, force=force)
    import_handler = handler_class(
        session=session,
        metadata_manager=metadata_manager,
        schemas=schemas,
        content_key=content_key,
        canonical_model=canonical_model,
        translation_model=translation_model,
        **handler_kwargs,
    )
    return Importer(
        directory=directory,
        session=session,
        fs_loader=load_translated_fs_state,
        db_loader=lambda: load_translated_db_state(
            session, translation_model, content_key
        ),
        handler=import_handler,
        metadata_manager=metadata_manager,
    )


def create_directory_translated_importer(
    directory,
    session,
    canonical_model,
    translation_model,
    node_model,
    schemas,
    content_key,
    content_reference_id,
    handler_class=ManifestBasedTranslatedHandler,
    force=False,
    **handler_kwargs,
):
    """
    Factory function for creating a ManifestBasedTranslatedImporter.

    Args:
        directory (str): Filesystem path to import from.
        session (Session): SQLAlchemy session.
        canonical_model: ORM model for canonical content.
        translation_model: ORM model for translations.
        node_model: ORM model for content nodes.
        schemas (dict): Schemas for manifest, canonical, translation, and node content.
        content_key (str): Attribute name for the canonical back-reference in translations.
        content_reference_id (str): Column name in node model for linking to translation.
        handler_class: Handler class to use (default: ManifestBasedTranslatedHandler).
        force (bool): Force metadata update.
        **handler_kwargs: Extra arguments for the handler.
    """  # noqa: E501
    metadata_manager = MetadataManager(session, force=force)
    import_handler = handler_class(
        session=session,
        metadata_manager=metadata_manager,
        schemas=schemas,
        content_key=content_key,
        canonical_model=canonical_model,
        translation_model=translation_model,
        node_model=node_model,
        content_reference_id=content_reference_id,
        **handler_kwargs,
    )
    return Importer(
        directory=directory,
        session=session,
        fs_loader=load_manifest_based_fs_state,
        db_loader=lambda: load_manifest_based_db_state(
            session, translation_model, content_key
        ),
        handler=import_handler,
        metadata_manager=metadata_manager,
    )
