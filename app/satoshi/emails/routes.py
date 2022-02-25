from flask import redirect, render_template, request, url_for

from app import cache
from app.models import Email, EmailThread
from app.satoshi.emails import bp


@bp.route("/", methods=["GET"])
@cache.cached()
def index():
    emails = Email.query.filter(Email.satoshi_id.isnot(None)).order_by(Email.date).all()
    return render_template("satoshi/emails/index.html", emails=emails)


@bp.route("/threads/", methods=["GET"])
@cache.cached()
def index_threads():
    threads = EmailThread.query.all()
    cryptography_threads = threads[0:2]
    bitcoin_list_threads = threads[2:]
    return render_template(
        "satoshi/emails/index_threads.html",
        threads=threads,
        cryptography_threads=cryptography_threads,
        bitcoin_list_threads=bitcoin_list_threads,
        source=None,
    )


@bp.route("/<string:source>/", methods=["GET"])
@cache.cached()
def index_source(source):
    emails = (
        Email.query.filter(Email.satoshi_id.isnot(None))
        .join(Email.email_thread, aliased=True)
        .filter_by(source=source)
        .order_by(Email.date)
        .all()
    )
    if len(emails) != 0:
        return render_template(
            "satoshi/emails/index.html", emails=emails, source=source
        )
    else:
        return redirect(url_for("satoshi.emails.index"))


@bp.route("/<string:source>/<int:email_id>/", methods=["GET"])
@cache.cached()
def detail(source, email_id):
    email = (
        Email.query.filter_by(satoshi_id=email_id)
        .join(Email.email_thread, aliased=True)
        .filter_by(source=source)
        .first()
    )
    previous_email = (
        Email.query.filter_by(satoshi_id=email_id - 1)
        .join(Email.email_thread, aliased=True)
        .first()
    )
    next_email = (
        Email.query.filter_by(satoshi_id=email_id + 1)
        .join(Email.email_thread, aliased=True)
        .first()
    )
    if email is not None:
        return render_template(
            "satoshi/emails/detail.html",
            email=email,
            previous_email=previous_email,
            next_email=next_email,
        )
    else:
        return redirect(url_for("satoshi.emails.index"))


@bp.route("/<string:source>/threads/", methods=["GET"])
@cache.cached()
def threads(source):
    threads = EmailThread.query.filter_by(source=source).order_by(EmailThread.id).all()
    if len(threads) > 0:
        return render_template(
            "satoshi/emails/index_threads.html", threads=threads, source=source
        )
    else:
        return redirect(url_for("satoshi.emails.index", view="threads"))


@bp.route(
    "/<string:source>/threads/<int:thread_id>/",
    methods=["GET"],
)
@cache.cached()
def detail_thread(source, thread_id):
    view_query = request.args.get("view")
    emails = Email.query.filter_by(thread_id=thread_id)
    if len(emails.all()) > 0:
        thread = emails[0].email_thread
        if thread.source != source:
            return redirect(
                url_for(
                    "satoshi.emails.detail_thread",
                    source=thread.source,
                    thread_id=thread_id,
                )
            )
    else:
        return redirect(url_for("satoshi.emails.index", view="threads"))
    if view_query == "satoshi":
        emails = emails.filter(Email.satoshi_id.isnot(None))
    emails = emails.all()
    previous_thread = EmailThread.query.filter_by(id=thread_id - 1).first()
    next_thread = EmailThread.query.filter_by(id=thread_id + 1).first()
    return render_template(
        "satoshi/emails/detail_thread.html",
        emails=emails,
        previous_thread=previous_thread,
        next_thread=next_thread,
    )
