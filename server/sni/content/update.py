from sni.authors.importers import AuthorImporter
from sni.library.importers import LibraryImporter
from sni.mempool.importers import MempoolImporter, MempoolSeriesImporter
from sni.podcast.importers import EpisodeImporter
from sni.satoshi.emails.importers import EmailImporter, EmailThreadImporter
from sni.satoshi.posts.importers import ForumPostImporter, ForumThreadImporter
from sni.satoshi.quotes.importers import QuoteCategoryImporter, QuoteImporter
from sni.skeptics.importers import SkepticImporter
from sni.translators.importers import TranslatorImporter


def update_content():
    importers = [
        AuthorImporter,
        TranslatorImporter,
        EmailImporter,
        EmailThreadImporter,
        ForumPostImporter,
        ForumThreadImporter,
        QuoteCategoryImporter,
        QuoteImporter,
        LibraryImporter,
        MempoolSeriesImporter,
        MempoolImporter,
        SkepticImporter,
        EpisodeImporter,
    ]
    for importer in importers:
        instance = importer()
        instance.run_import()
