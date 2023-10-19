from sni.library.models import document_authors, document_formats, document_translators
from sni.mempool.models import blog_post_authors, blog_post_translators
from sni.satoshi.quotes.models import quote_quote_categories


def make_shell_context():
    return {
        "blog_post_authors": blog_post_authors,
        "blog_post_translators": blog_post_translators,
        "document_authors": document_authors,
        "document_formats": document_formats,
        "document_translators": document_translators,
        "quote_quote_categories": quote_quote_categories,
    }
