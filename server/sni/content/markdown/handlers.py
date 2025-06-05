import os

from sqlalchemy import select

from sni.content.metadata import Actions
from sni.models import MarkdownContent
from sni.utils.files import split_filename

from .file_processor import process_file


class BasicHandler:
    def __init__(self, session, metadata_manager, schema, canonical_model):
        self.session = session
        self.metadata_manager = metadata_manager
        self.schema = schema
        self.canonical_model = canonical_model

    def handle_new(self, filepath, fs_record):
        new_metadata = self.metadata_manager.create_metadata(filepath)
        results, html, file_content = process_file(filepath, {"canonical": self.schema})
        canonical_data = results["canonical"].data
        canonical_data = self.process_canonical_data(canonical_data, fs_record)

        slug, *_ = split_filename(os.path.basename(filepath))
        new_content = MarkdownContent(
            file_content=file_content,
            html_content=html,
            file_metadata=new_metadata,
        )
        self.session.add(new_content)
        self.session.flush()

        new_entry = self.canonical_model(
            **canonical_data,
            slug=slug,
            content=new_content,
        )
        self.session.add(new_entry)

    def handle_deleted(self, db_entry):
        self.session.delete(db_entry)
        self.metadata_manager.record_action(Actions.DELETED)

    def handle_existing(self, filepath, fs_record, db_entry):
        old_metadata = db_entry.content.file_metadata
        action, new_metadata = self.metadata_manager.update_metadata(
            filepath, old_metadata
        )
        if action != Actions.UPDATED:
            return

        results, html, file_content = process_file(filepath, {"canonical": self.schema})
        canonical_data = results["canonical"].data
        canonical_data = self.process_canonical_data(canonical_data, fs_record)

        slug, *_ = split_filename(os.path.basename(filepath))

        db_entry.content.file_content = file_content
        db_entry.content.html_content = html
        db_entry.content.file_metadata = new_metadata
        for key, value in canonical_data.items():
            setattr(db_entry, key, value)
        db_entry.slug = slug

    def process_canonical_data(self, canonical_data, fs_record):
        return canonical_data


class TranslatedHandler:
    def __init__(
        self,
        session,
        metadata_manager,
        schemas,
        content_key,
        canonical_model,
        translation_model,
    ):
        self.session = session
        self.metadata_manager = metadata_manager
        self.schemas = schemas
        self.content_key = content_key
        self.canonical_model = canonical_model
        self.translation_model = translation_model

    def handle_new(self, slug, fs_record):
        en_file = fs_record.get("en")
        if not en_file:
            print(f"Skipping slug {slug}: no canonical (en) file.")
            return

        # Create canonical entry
        new_metadata = self.metadata_manager.create_metadata(en_file)
        results, html, content = process_file(en_file, self.schemas)
        canonical_data = results["canonical"].data
        canonical_data = self.process_canonical_data(canonical_data, fs_record)

        canonical_entry = self.canonical_model(slug=slug, **canonical_data)
        self.session.add(canonical_entry)

        translation_data = results["translation"].data
        translation_data = self.process_translation_data(
            translation_data, "en", None, fs_record
        )
        translation_data.pop("slug", None)

        new_content = MarkdownContent(
            file_content=content,
            html_content=html,
            file_metadata=new_metadata,
        )
        self.session.add(new_content)

        en_translation = self.translation_model(
            slug=slug,
            locale="en",
            content=new_content,
            **{self.content_key: canonical_entry},
            **translation_data,
        )
        self.session.add(en_translation)

        # Create other translations
        for locale, fpath in fs_record.items():
            if locale == "en":
                continue
            self._create_translation(fpath, slug, locale, en_translation, fs_record)

    def handle_deleted(self, db_entry):
        self.session.delete(db_entry["canonical"])
        self.metadata_manager.record_action(Actions.DELETED)

    def handle_existing(self, slug, fs_record, db_entry):
        canonical_entry = db_entry["canonical"]
        translations = db_entry["translations"]

        fs_locales = set(fs_record.keys())
        db_locales = set(translations.keys())

        new_locales = fs_locales - db_locales
        deleted_locales = db_locales - fs_locales
        existing_locales = fs_locales & db_locales

        # Update canonical and English translation
        if "en" in fs_locales:
            en_file = fs_record["en"]
            en_translation = translations.get("en")
            self._update_canonical(en_file, canonical_entry, en_translation, fs_record)

        # New and updated translations (excluding English, already handled)
        for locale in new_locales | existing_locales:
            if locale == "en":
                continue
            fpath = fs_record[locale]
            db_translation = translations.get(locale)
            if locale in new_locales:
                self._create_translation(fpath, slug, locale, db_translation, fs_record)
            else:
                self._update_translation(
                    fpath, db_translation, locale, db_translation, fs_record
                )

        # Deleted translations
        for locale in deleted_locales:
            self.session.delete(translations[locale])
            self.metadata_manager.record_action(Actions.DELETED)
            if locale == "en":
                self.session.delete(canonical_entry)

    def _update_canonical(self, filepath, canonical_entry, en_translation, fs_record):
        old_metadata = en_translation.content.file_metadata if en_translation else None
        action, new_metadata = self.metadata_manager.update_metadata(
            filepath, old_metadata
        )
        if action != Actions.UPDATED:
            return

        results, html, content = process_file(filepath, self.schemas)
        canonical_data = results["canonical"].data
        translation_data = results["translation"].data

        canonical_data = self.process_canonical_data(canonical_data, fs_record)
        for k, v in canonical_data.items():
            setattr(canonical_entry, k, v)

        if en_translation:
            en_translation.content.file_content = content
            en_translation.content.html_content = html
            en_translation.content.file_metadata = new_metadata
            translation_data.pop("slug", None)
            translation_data = self.process_translation_data(
                translation_data, "en", en_translation, fs_record
            )
            for k, v in translation_data.items():
                setattr(en_translation, k, v)
        else:
            new_content = MarkdownContent(
                file_content=content,
                html_content=html,
                file_metadata=new_metadata,
            )
            self.session.add(new_content)
            en_translation = self.translation_model(
                slug=canonical_entry.slug,
                locale="en",
                content=new_content,
                **{self.content_key: canonical_entry},
                **translation_data,
            )
            self.session.add(en_translation)

    def _create_translation(
        self, filepath, slug, locale, canonical_translation, fs_record
    ):
        new_metadata = self.metadata_manager.create_metadata(filepath)
        results, html, content = process_file(
            filepath, {"translation": self.schemas["translation"]}
        )
        translation_data = results["translation"].data
        translation_data["slug"] = translation_data.get("slug") or slug
        translation_data = self.process_translation_data(
            translation_data, locale, canonical_translation, fs_record
        )

        new_content = MarkdownContent(
            file_content=content,
            html_content=html,
            file_metadata=new_metadata,
        )
        self.session.add(new_content)

        translation_entry = self.translation_model(
            locale=locale,
            content=new_content,
            **{self.content_key: getattr(canonical_translation, self.content_key)},
            **translation_data,
        )
        self.session.add(translation_entry)

    def _update_translation(
        self, filepath, db_translation, locale, canonical_translation, fs_record
    ):
        old_metadata = db_translation.content.file_metadata
        action, new_metadata = self.metadata_manager.update_metadata(
            filepath, old_metadata
        )
        if action != Actions.UPDATED:
            return

        results, html, content = process_file(
            filepath, {"translation": self.schemas["translation"]}
        )
        translation_data = results["translation"].data
        translation_data["slug"] = (
            translation_data.get("slug") or canonical_translation.slug
        )
        translation_data = self.process_translation_data(
            translation_data, locale, canonical_translation, fs_record
        )

        db_translation.content.file_content = content
        db_translation.content.html_content = html
        db_translation.content.file_metadata = new_metadata
        for k, v in translation_data.items():
            setattr(db_translation, k, v)

    def process_canonical_data(self, canonical_data, fs_record):
        """
        Hook for tweaking canonical data. Override if needed.
        """
        return canonical_data

    def process_translation_data(
        self, translation_data, locale, canonical_translation, fs_record
    ):
        """
        Hook for tweaking translation data. Override if needed.
        """
        return translation_data


def select_schemas(schemas: dict, *keys: str) -> dict:
    return {k: schemas[k] for k in keys}


class ManifestBasedTranslatedHandler:
    def __init__(
        self,
        session,
        metadata_manager,
        schemas,
        content_key,
        canonical_model,
        translation_model,
        node_model,
        content_reference_id,
    ):
        self.session = session
        self.metadata_manager = metadata_manager
        self.schemas = schemas
        self.content_key = content_key
        self.canonical_model = canonical_model
        self.translation_model = translation_model
        self.node_model = node_model
        self.content_reference_id = content_reference_id

    def handle_new(self, slug, fs_record):
        manifest_file = fs_record["manifest"]
        content_dir = fs_record["content_dir"]
        directory = fs_record["directory"]

        # Process manifest and content
        new_metadata = self.metadata_manager.create_metadata(directory)
        schemas = select_schemas(self.schemas, "manifest", "canonical", "translation")
        results, html_content, file_content = process_file(manifest_file, schemas)
        manifest_data = results["manifest"].model
        canonical_data = results["canonical"].data
        translation_data = results["translation"].data

        # Canonical entry
        canonical_data = self.process_canonical_data(canonical_data, fs_record)
        canonical_entry = self.canonical_model(slug=slug, **canonical_data)
        self.session.add(canonical_entry)
        self.session.flush()

        # English translation entry
        translation_data = self.process_translation_data(
            translation_data, "en", None, fs_record
        )
        translation_data.pop("slug", None)

        new_content = MarkdownContent(
            file_content=file_content,
            html_content=html_content,
            file_metadata=new_metadata,
        )
        self.session.add(new_content)

        en_translation = self.translation_model(
            slug=slug,
            locale="en",
            content=new_content,
            **{self.content_key: canonical_entry},
            **translation_data,
        )
        self.session.add(en_translation)
        self.session.flush()

        # Insert nodes
        self._insert_nodes(manifest_data.nodes, None, en_translation.id, 1, content_dir)

    def handle_deleted(self, db_entry):
        self.session.delete(db_entry["canonical"])
        self.metadata_manager.record_action(Actions.DELETED)

    def handle_existing(self, slug, fs_record, db_entry):
        manifest_file = fs_record["manifest"]
        content_dir = fs_record["content_dir"]
        directory = fs_record["directory"]

        canonical_entry = db_entry["canonical"]
        en_translation = db_entry["translations"].get("en")

        old_metadata = en_translation.content.file_metadata if en_translation else None
        action, new_metadata = self.metadata_manager.update_metadata(
            directory, old_metadata
        )
        if action != Actions.UPDATED:
            return

        results, html_content, file_content = process_file(manifest_file, self.schemas)
        manifest_data = results["manifest"].model
        canonical_data = results["canonical"].data
        translation_data = results["translation"].data

        # Update canonical entry
        canonical_data = self.process_canonical_data(canonical_data, fs_record)
        for k, v in canonical_data.items():
            setattr(canonical_entry, k, v)
        self.session.add(canonical_entry)

        # Update English translation entry
        if en_translation:
            en_translation.content.file_content = file_content
            en_translation.content.html_content = html_content
            en_translation.content.file_metadata = new_metadata

            translation_data = self.process_translation_data(
                translation_data, "en", None, fs_record
            )
            translation_data.pop("slug", None)

            for k, v in translation_data.items():
                setattr(en_translation, k, v)
            self.session.add(en_translation)
        else:
            # Create new English translation
            new_content = MarkdownContent(
                file_content=file_content,
                html_content=html_content,
                file_metadata=new_metadata,
            )
            self.session.add(new_content)
            en_translation = self.translation_model(
                slug=slug,
                locale="en",
                content=new_content,
                **{self.content_key: canonical_entry},
                **translation_data,
            )
            self.session.add(en_translation)
            self.session.flush()

        # Delete and recreate nodes
        self._delete_existing_nodes(en_translation.id)
        self._insert_nodes(manifest_data.nodes, None, en_translation.id, 1, content_dir)

    def process_canonical_data(self, canonical_data, fs_record):
        return canonical_data

    def process_translation_data(
        self, translation_data, locale, canonical_translation, fs_record
    ):
        return translation_data

    def _delete_existing_nodes(self, content_reference_id):
        nodes_to_delete = self.session.scalars(
            select(self.node_model).filter_by(
                **{self.content_reference_id: content_reference_id}
            )
        ).all()
        for node in nodes_to_delete:
            self.session.delete(node)
        self.session.commit()

    def _insert_nodes(
        self, node_data, parent_id, content_reference_id, order, content_dir
    ):
        if isinstance(node_data, list):
            for idx, child in enumerate(node_data, start=1):
                self._insert_nodes(
                    child, parent_id, content_reference_id, idx, content_dir
                )
        elif isinstance(node_data, str):
            node = self._insert_node(
                node_data, order, parent_id, content_reference_id, content_dir
            )
            return node.id
        elif hasattr(node_data, "slug") and hasattr(node_data, "children"):
            node = self._insert_node(
                node_data.slug, order, parent_id, content_reference_id, content_dir
            )
            node_id = node.id
            for idx, child in enumerate(node_data.children, start=1):
                self._insert_nodes(
                    child, node_id, content_reference_id, idx, content_dir
                )
            return node_id

    def _insert_node(self, slug, order, parent_id, content_reference_id, content_dir):
        md_file = os.path.join(content_dir, f"{slug}.md")
        schemas = select_schemas(self.schemas, "node_content")
        results, html_content, file_content = process_file(md_file, schemas)
        node_data = results["node_content"].data

        node = self.node_model(
            slug=slug,
            **node_data,
            order=order,
            html_content=html_content,
            file_content=file_content,
            parent_id=parent_id,
            **{self.content_reference_id: content_reference_id},
        )
        self.session.add(node)
        self.session.commit()

        return node
