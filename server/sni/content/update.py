from sni.authors.importers import import_author
from sni.library.importers import import_library
from sni.mempool.importers import import_mempool, import_mempool_series
from sni.podcast.importers import import_episode
from sni.satoshi.emails.importers import import_email, import_email_thread
from sni.satoshi.posts.importers import import_forum_post, import_forum_thread
from sni.satoshi.quotes.importers import import_quote, import_quote_category
from sni.skeptics.importers import import_skeptic
from sni.translators.importers import import_translator


def update_content():
    import_author()
    import_translator()
    import_email()
    import_email_thread()
    import_forum_post()
    import_forum_thread()
    import_quote_category()
    import_quote()
    import_library()
    import_mempool_series()
    import_mempool()
    import_skeptic()
    import_episode()
