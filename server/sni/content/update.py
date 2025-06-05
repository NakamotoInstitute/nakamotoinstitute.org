from sni.authors.importers import import_authors
from sni.database import session_scope
from sni.library.importers import (
    import_library,
    import_library_books,
    import_library_weights,
)
from sni.mempool.importers import import_mempool_posts, import_mempool_series
from sni.podcasts.importers import import_episodes, import_podcasts
from sni.satoshi.emails.importers import import_email_threads, import_emails
from sni.satoshi.posts.importers import import_forum_posts, import_forum_threads
from sni.satoshi.quotes.importers import import_quote_categories, import_quotes
from sni.skeptics.importers import import_skeptics
from sni.translators.importers import import_translators


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
    import_authors("content/authors", force)
    import_translators("content/translators", force)
    import_mempool_series("content/mempool_series", force)
    import_mempool_posts("content/mempool", force)
    import_library("content/library", force)
    import_library_books("content/library_books", force)
    import_podcasts("content/podcasts", force)
    import_episodes("content/podcast_episodes", force)

    with session_scope() as session:
        import_library_weights(session, force=True)
