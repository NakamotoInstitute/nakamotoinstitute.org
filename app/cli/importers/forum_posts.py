import click

from app import db
from app.cli.utils import DONE, load_and_validate_json
from app.models import ForumPost, ForumThread
from app.satoshi.posts.schemas import ForumPostJSONSchema, ForumThreadJSONSchema


def import_forum_thread():
    click.echo("Importing ForumThread...", nl=False)
    forum_threads_data = load_and_validate_json(
        "data/forum_threads.json", ForumThreadJSONSchema
    )
    for forum_thread_data in forum_threads_data:
        email_thread = ForumThread(**forum_thread_data.dict())
        db.session.add(email_thread)
    db.session.commit()
    click.echo(DONE)


def import_forum_post():
    click.echo("Importing ForumPost...", nl=False)
    forum_posts_data = load_and_validate_json("data/posts.json", ForumPostJSONSchema)
    for forum_post_data in forum_posts_data:
        forum_post = ForumPost(**forum_post_data.dict())
        db.session.add(forum_post)
    db.session.commit()
    click.echo(DONE)
