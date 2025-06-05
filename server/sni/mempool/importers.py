from sni.content.markdown import TranslatedHandler, create_translated_importer
from sni.database import SessionLocalSync
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
    MempoolSeriesCanonicalMDModel,
    MempoolSeriesTranslationMDModel,
    MempoolTranslationMDModel,
)


class MempoolHandler(TranslatedHandler):
    def process_canonical_data(self, canonical_data, fs_record):
        canonical_data["authors"] = [
            get(Author, db_session=self.session, slug=author)
            for author in canonical_data.pop("authors")
        ]
        series = canonical_data.pop("series")
        canonical_data["series"] = (
            get(BlogSeriesTranslation, db_session=self.session, slug=series).blog_series
            if series
            else None
        )
        return canonical_data

    def process_translation_data(
        self, translation_data, locale, canonical_translation, fs_record
    ):
        translation_data["translators"] = [
            get(Translator, db_session=self.session, slug=slug)
            for slug in translation_data.pop("translators", [])
        ]
        if locale != "en":
            translation_data["excerpt"] = (
                translation_data.get("excerpt") or canonical_translation.excerpt
            )
        return translation_data


def import_mempool_posts(directory: str, force: bool = False):
    with SessionLocalSync() as session:
        importer = create_translated_importer(
            directory=directory,
            session=session,
            handler_class=MempoolHandler,
            canonical_model=BlogPost,
            translation_model=BlogPostTranslation,
            schemas={
                "canonical": MempoolCanonicalMDModel,
                "translation": MempoolTranslationMDModel,
            },
            content_key="blog_post",
            force=force,
        )
        importer.run()


def import_mempool_series(directory: str, force: bool = False):
    with SessionLocalSync() as session:
        importer = create_translated_importer(
            directory=directory,
            session=session,
            canonical_model=BlogSeries,
            translation_model=BlogSeriesTranslation,
            schemas={
                "canonical": MempoolSeriesCanonicalMDModel,
                "translation": MempoolSeriesTranslationMDModel,
            },
            content_key="blog_series",
            force=force,
        )
        importer.run()
