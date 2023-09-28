from typing import List

from app import db
from app.models import Email
from app.utils.decorators import response_model

from . import bp
from .schemas import EmailResponse


@bp.route("/", methods=["GET"])
@response_model(List[EmailResponse])
def get_emails():
    emails = db.session.scalars(
        db.select(Email).filter(Email.satoshi_id.isnot(None)).order_by(Email.date)
    ).all()
    return emails
