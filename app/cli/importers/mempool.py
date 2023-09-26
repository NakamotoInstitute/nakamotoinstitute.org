from app.cli.utils import import_content
from app.mempool.schemas import MempoolMDSchema, MempoolTranslatedMDSchema
from app.models import BlogPost, BlogPostTranslation


def import_mempool():
    import_content(
        "content/mempool",
        MempoolMDSchema,
        MempoolTranslatedMDSchema,
        BlogPost,
        BlogPostTranslation,
        "blog_post",
    )
