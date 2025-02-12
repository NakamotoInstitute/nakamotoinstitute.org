from sni.authors.importers import AuthorImporter
from sni.database import session_scope
from sni.library.importers import (
    LibraryBookImporter,
    LibraryImporter,
    import_library_weights,
)
from sni.mempool.importers import MempoolImporter, MempoolSeriesImporter
from sni.podcasts.importers import EpisodeImporter, PodcastImporter
from sni.satoshi.emails.importers import import_email_threads, import_emails
from sni.satoshi.posts.importers import import_forum_posts, import_forum_threads
from sni.satoshi.quotes.importers import import_quote_categories, import_quotes
from sni.skeptics.importers import import_skeptics
from sni.translators.importers import TranslatorImporter


def update_content(force: bool = False):
    with session_scope() as db_session:
        # Import emails
        email_thread_updated = import_email_threads(db_session, force)
        import_emails(db_session, force, [email_thread_updated])

        # Import forum posts
        forum_thread_updated = import_forum_threads(db_session, force)
        import_forum_posts(db_session, force, [forum_thread_updated])

        # Import quotes
        quote_category_updated = import_quote_categories(db_session, force)
        import_quotes(db_session, force, [quote_category_updated])

        # Import skeptics
        import_skeptics(db_session, force)

        # Import markdown content
        importers = [
            AuthorImporter,
            TranslatorImporter,
            LibraryImporter,
            LibraryBookImporter,
            MempoolSeriesImporter,
            MempoolImporter,
            PodcastImporter,
            EpisodeImporter,
        ]
        for importer in importers:
            instance = importer()
            instance.run_import(force)

        import_library_weights(db_session, force=True)
