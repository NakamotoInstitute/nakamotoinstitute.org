import click

from app import db
from app.cli.utils import DONE, load_all_markdown_files
from app.models import Episode
from app.podcast.schemas import EpisodeMDModel


def import_episode():
    click.echo("Importing Episode...", nl=False)
    episodes_data = load_all_markdown_files("content/podcast", EpisodeMDModel)
    for episode_data in episodes_data:
        episode = Episode(**episode_data)
        db.session.add(episode)
    db.session.commit()
    click.echo(DONE)
