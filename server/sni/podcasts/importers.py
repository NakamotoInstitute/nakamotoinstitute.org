from sni.content.markdown import MarkdownImporter
from sni.models import Episode, Podcast
from sni.shared.service import get

from .schemas import EpisodeMDModel, PodcastMDModel


class PodcastImporter(MarkdownImporter):
    directory_path = "content/podcasts"
    content_type = "Podcast"
    model = Podcast
    schema = PodcastMDModel
    content_key = "podcast"


def import_podcast():
    podcast_importer = PodcastImporter()
    podcast_importer.run_import()


class EpisodeImporter(MarkdownImporter):
    directory_path = "content/podcast_episodes"
    content_type = "Episode"
    model = Episode
    schema = EpisodeMDModel
    content_key = "episode"

    def process_canonical_additional_data(self, canonical_data):
        canonical_data["podcast"] = get(
            Podcast, db_session=self.db_session, slug=canonical_data.pop("podcast")
        )
        return canonical_data


def import_episode():
    episode_importer = EpisodeImporter()
    episode_importer.run_import()
