from sni.cli.utils import TranslatedContentImporter
from sni.mempool.models import BlogSeries, BlogSeriesTranslation
from sni.mempool.schemas import (
    MempoolSeriesCanonicalMDModel,
    MempoolSeriesMDModel,
    MempoolSeriesTranslationMDModel,
)


class MempoolSeriesImporter(TranslatedContentImporter):
    content_type = "Mempool series"
    canonical_model = BlogSeries
    translation_model = BlogSeriesTranslation
    canonical_schema = MempoolSeriesCanonicalMDModel
    md_schema = MempoolSeriesMDModel
    translation_schema = MempoolSeriesTranslationMDModel
    content_key = "blog_series"


def import_mempool_series():
    mempool_series_importer = MempoolSeriesImporter(
        directory_path="content/mempool_series"
    )
    mempool_series_importer.run_import()
