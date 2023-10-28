from sni.authors.models import Author
from sni.cli.utils import TranslatedContentImporter, get
from sni.mempool.models import BlogPost, BlogPostTranslation, BlogSeriesTranslation
from sni.mempool.schemas import (
    MempoolCanonicalMDModel,
    MempoolMDModel,
    MempoolTranslationMDModel,
)
from sni.translators.models import Translator


class MempoolImporter(TranslatedContentImporter):
    content_type = "Mempool"
    canonical_model = BlogPost
    translation_model = BlogPostTranslation
    canonical_schema = MempoolCanonicalMDModel
    md_schema = MempoolMDModel
    translation_schema = MempoolTranslationMDModel
    content_key = "blog_post"

    def process_canonical_additional_data(self, canonical_data):
        canonical_data["authors"] = [
            get(Author, slug=author) for author in canonical_data.pop("authors")
        ]
        series = canonical_data.pop("series")
        canonical_data["series"] = (
            get(BlogSeriesTranslation, slug=series).blog_series if series else None
        )
        return canonical_data

    def process_translation_additional_data(
        self, translation_data, canonical_entry, metadata
    ):
        translation_data["translators"] = [
            get(Translator, slug=slug)
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
            get(Translator, slug=slug)
            for slug in translation_data.pop("translators", [])
        ]

        return super().process_translation_for_translated_file(
            translation_data, canonical_entry, metadata
        )


def import_mempool():
    mempool_importer = MempoolImporter(directory_path="content/mempool")
    mempool_importer.run_import()
