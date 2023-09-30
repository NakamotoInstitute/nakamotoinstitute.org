from typing import List

from app import db
from app.models import Episode
from app.utils.decorators import response_model

from . import bp
from .schemas import EpisodeResponse


@bp.route("/", methods=["GET"])
@response_model(List[EpisodeResponse])
def get_episodes():
    episodes = db.session.scalars(
        db.select(Episode).order_by(Episode.date.desc())
    ).all()
    return episodes


@bp.route("/<string:slug>", methods=["GET"])
@response_model(EpisodeResponse)
def get_episode(slug):
    episode = db.first_or_404(db.select(Episode).filter_by(slug=slug))
    return episode
