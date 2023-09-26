import click

from app.cli.utils import DONE, import_content
from app.mempool.schemas import MempoolMDSchema, MempoolTranslatedMDSchema
from app.models import BlogPost, BlogPostTranslation


def import_mempool():
    click.echo("Importing Mempool...", nl=False)
    import_content(
        "content/mempool",
        MempoolMDSchema,
        MempoolTranslatedMDSchema,
        BlogPost,
        BlogPostTranslation,
        ["title", "excerpt", "image_alt"],
        "blog_post",
    )
    click.echo(DONE)
