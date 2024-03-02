from sni.content.markdown import TranslatedMarkdownImporter
from sni.models import (
    Author,
    BlogPost,
    BlogPostTranslation,
    BlogSeries,
    BlogSeriesTranslation,
    Translator,
)
from sni.shared.service import get

from .schemas import (
    MempoolCanonicalMDModel,
    MempoolMDModel,
    MempoolSeriesCanonicalMDModel,
    MempoolSeriesMDModel,
    MempoolSeriesTranslationMDModel,
    MempoolTranslationMDModel,
)


class MempoolImporter(TranslatedMarkdownImporter):
    directory_path = "content/mempool"
    content_type = "Mempool"
    canonical_model = BlogPost
    translation_model = BlogPostTranslation
    canonical_schema = MempoolCanonicalMDModel
    md_schema = MempoolMDModel
    translation_schema = MempoolTranslationMDModel
    content_key = "blog_post"

    def process_canonical_additional_data(self, canonical_data):
        canonical_data["authors"] = [
            get(Author, db_session=self.db_session, slug=author)
            for author in canonical_data.pop("authors")
        ]
        series = canonical_data.pop("series")
        canonical_data["series"] = (
            get(
                BlogSeriesTranslation, db_session=self.db_session, slug=series
            ).blog_series
            if series
            else None
        )
        return canonical_data

    def process_translation_additional_data(
        self, translation_data, canonical_entry, metadata
    ):
        translation_data["translators"] = [
            get(Translator, db_session=self.db_session, slug=slug)
            for slug in translation_data.pop("translators", [])
        ]
        return super().process_translation_additional_data(
            translation_data, canonical_entry, metadata
        )

    def process_translation_for_translated_file(
        self, translation_data, canonical_entry, metadata
    ):
        translation_data["excerpt"] = (
            translation_data.get("excerpt") or canonical_entry["translation"].excerpt
        )
        translation_data["translators"] = [
            get(Translator, db_session=self.db_session, slug=slug)
            for slug in translation_data.pop("translators", [])
        ]

        return super().process_translation_for_translated_file(
            translation_data, canonical_entry, metadata
        )


def import_mempool():
    mempool_importer = MempoolImporter()
    mempool_importer.run_import()


class MempoolSeriesImporter(TranslatedMarkdownImporter):
    directory_path = "content/mempool_series"
    content_type = "Mempool series"
    canonical_model = BlogSeries
    translation_model = BlogSeriesTranslation
    canonical_schema = MempoolSeriesCanonicalMDModel
    md_schema = MempoolSeriesMDModel
    translation_schema = MempoolSeriesTranslationMDModel
    content_key = "blog_series"


def import_mempool_series():
    mempool_series_importer = MempoolSeriesImporter()
    mempool_series_importer.run_import()
