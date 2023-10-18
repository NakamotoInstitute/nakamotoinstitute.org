import click

from sni.cli.utils import DONE, load_and_validate_json
from sni.extensions import db
from sni.models import ForumPost, ForumThread
from sni.satoshi.posts.schemas import ForumPostJSONModel, ForumThreadJSONModel


def import_forum_thread():
    click.echo("Importing ForumThread...", nl=False)
    forum_threads_data = load_and_validate_json(
        "data/forum_threads.json", ForumThreadJSONModel
    )
    for forum_thread_data in forum_threads_data:
        email_thread = ForumThread(**forum_thread_data.dict())
        db.session.add(email_thread)
    db.session.commit()
    click.echo(DONE)


def import_forum_post():
    click.echo("Importing ForumPost...", nl=False)
    forum_posts_data = load_and_validate_json(
        "data/forum_posts.json", ForumPostJSONModel
    )
    for forum_post_data in forum_posts_data:
        forum_post = ForumPost(**forum_post_data.dict())
        db.session.add(forum_post)
    db.session.commit()
    click.echo(DONE)
