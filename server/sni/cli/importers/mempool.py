from sni.authors.models import Author
from sni.cli.utils import (
    ContentImporter,
    get,
    process_canonical_file,
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

    def process_and_add_canonical_file(self, filepath, slug):
        (
            validated_canonical_data,
            validated_translation_data,
            content,
        ) = process_canonical_file(filepath, self.canonical_schema, self.md_schema)

        canonical_data = validated_canonical_data.dict()
        translation_data = validated_translation_data.dict()

        canonical_data["authors"] = [
            get(Author, slug=author) for author in canonical_data.pop("authors")
        ]
        series = canonical_data.pop("series")
        canonical_data["series"] = (
            get(BlogSeriesTranslation, slug=series).blog_series if series else None
        )
        blog_post = self.canonical_model(**canonical_data)
        db.session.add(blog_post)
        db.session.flush()

        translation_data["translators"] = [
            get(Translator, slug=slug)
            for slug in translation_data.pop("translators", [])
        ]
        blog_post_translation = self.translation_model(
            **translation_data,
            slug=slug,
            locale="en",
            content=content,
            blog_post=blog_post,
        )
        db.session.add(blog_post_translation)

        self.content_map[slug] = {
            "canonical": blog_post,
            "translation": blog_post_translation,
        }

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
