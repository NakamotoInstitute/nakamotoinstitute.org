from sni.cli.utils import ContentImporter
from sni.podcast.models import Episode
from sni.podcast.schemas import EpisodeMDModel


class EpisodeImporter(ContentImporter):
    content_type = "Episode"
    model = Episode
    schema = EpisodeMDModel
    content_key = "episode"


def import_episode():
    episode_importer = EpisodeImporter(directory_path="content/podcast")
    episode_importer.run_import()
