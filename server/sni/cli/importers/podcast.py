import click

from sni.cli.utils import DONE, load_all_markdown_files
from sni.extensions import db
from sni.models import Episode
from sni.podcast.schemas import EpisodeMDModel


def import_episode():
    click.echo("Importing Episode...", nl=False)
    episodes_data = load_all_markdown_files("content/podcast", EpisodeMDModel)
    for episode_data in episodes_data:
        episode = Episode(**episode_data)
        db.session.add(episode)
    db.session.commit()
    click.echo(DONE)
