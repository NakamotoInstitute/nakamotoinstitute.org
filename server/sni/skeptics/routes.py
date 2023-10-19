from typing import List

from flask import Blueprint

from sni.extensions import db
from sni.skeptics.models import Skeptic
from sni.utils.decorators import response_model

from .schemas import SkepticModel

blueprint = Blueprint("skeptics", __name__, url_prefix="/skeptics")


@blueprint.route("/", methods=["GET"])
@response_model(List[SkepticModel])
def get_skeptics():
    skeptics = db.session.scalars(db.select(Skeptic).order_by(Skeptic.date)).all()
    return skeptics
