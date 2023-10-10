from typing import List

from flask import jsonify

from sni import db
from sni.models import Email, EmailThread
from sni.utils.decorators import response_model
from sni.utils.request import get_bool_param

from . import bp
from .schemas import (
    EmailBaseModel,
    EmailDetailModel,
    EmailThreadBaseModel,
    EmailThreadModel,
    SatoshiEmailModel,
)


@bp.route("/", methods=["GET"])
@response_model(List[EmailBaseModel])
def get_emails():
    emails = db.session.scalars(
        db.select(Email).filter(Email.satoshi_id.isnot(None)).order_by(Email.date)
    ).all()
    return emails


@bp.route("/threads", methods=["GET"])
@response_model(List[EmailThreadBaseModel])
def get_email_threads():
    threads = db.session.scalars(db.select(EmailThread)).all()
    return threads


@bp.route("/<string:source>", methods=["GET"])
@response_model(List[SatoshiEmailModel])
def get_emails_by_source(source):
    emails = db.session.scalars(
        db.select(Email)
        .filter(Email.satoshi_id.isnot(None))
        .join(EmailThread)
        .filter_by(source=source)
        .order_by(Email.date)
    ).all()
    return emails


@bp.route("/<string:source>/<int:satoshi_id>", methods=["GET"])
def get_email_by_source(source, satoshi_id):
    email = db.first_or_404(
        db.select(Email)
        .filter_by(satoshi_id=satoshi_id)
        .join(EmailThread)
        .filter_by(source=source)
    )
    previous_email = db.session.scalar(
        db.select(Email).filter_by(satoshi_id=satoshi_id - 1).join(EmailThread)
    )
    next_email = db.session.scalar(
        db.select(Email).filter_by(satoshi_id=satoshi_id + 1).join(EmailThread)
    )

    response_data = EmailDetailModel(
        email=email, previous=previous_email, next=next_email
    )

    return jsonify(response_data.dict(by_alias=True))


@bp.route("/<string:source>/threads", methods=["GET"])
@response_model(List[EmailThreadBaseModel])
def get_email_threads_by_source(source):
    threads = db.session.scalars(
        db.select(EmailThread).filter_by(source=source).order_by(EmailThread.id)
    ).all()
    return threads


@bp.route("/<string:source>/threads/<int:thread_id>", methods=["GET"])
def get_email_thread_by_source(source, thread_id):
    satoshi_only = get_bool_param("satoshi")

    emails_query = (
        db.select(Email)
        .join(EmailThread)
        .filter(Email.thread_id == thread_id, EmailThread.source == source)
    )
    if satoshi_only:
        emails_query = emails_query.filter(Email.satoshi_id.isnot(None))
    emails = db.session.scalars(emails_query).all()

    thread = emails[0].thread

    previous_thread = db.session.scalar(
        db.select(EmailThread).filter_by(id=thread_id - 1)
    )
    next_thread = db.session.scalar(db.select(EmailThread).filter_by(id=thread_id + 1))

    response_data = EmailThreadModel(
        emails=emails, thread=thread, previous=previous_thread, next=next_thread
    )

    return jsonify(response_data.dict(by_alias=True))
