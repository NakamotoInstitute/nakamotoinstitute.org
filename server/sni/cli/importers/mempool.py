from sni.authors.models import Author
from sni.cli.utils import (
    ContentImporter,
    get,
    process_translated_file,
)
from sni.extensions import db
from sni.mempool.models import BlogPost, BlogPostTranslation, BlogSeriesTranslation
from sni.mempool.schemas import (
    MempoolCanonicalMDModel,
    MempoolMDModel,
    MempoolTranslationMDModel,
)
from sni.translators.models import Translator


class MempoolImporter(ContentImporter):
    content_type = "mempool"
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
        self, translation_data, canonical_entry, slug, content
    ):
        translation_data["translators"] = [
            get(Translator, slug=slug)
            for slug in translation_data.pop("translators", [])
        ]
        return translation_data

    def process_and_add_translated_file(self, filepath, slug, locale):
        validated_translation_data, content = process_translated_file(
            filepath, self.translation_schema
        )

        translation_data = validated_translation_data.dict()
        blog_post = self.content_map.get(slug)

        if not blog_post:
            return

        translation_data["slug"] = translation_data.get("slug") or slug
        translation_data["excerpt"] = (
            translation_data.get("excerpt") or blog_post["translation"].excerpt
        )
        translation_data["translators"] = [
            get(Translator, slug=slug)
            for slug in translation_data.pop("translators", [])
        ]
        blog_post_translation = self.translation_model(
            **translation_data,
            locale=locale,
            content=content,
            blog_post=blog_post["canonical"],
        )
        db.session.add(blog_post_translation)


def import_mempool():
    mempool_importer = MempoolImporter(directory_path="content/mempool")
    mempool_importer.run_import()
