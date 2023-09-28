import click

from app import db
from app.cli.utils import DONE, load_and_validate_json
from app.models import Email, EmailThread
from app.satoshi.emails.schemas import EmailJSONSchema, EmailThreadJSONSchema


def import_email_thread():
    click.echo("Importing EmailThread...", nl=False)
    email_threads_data = load_and_validate_json(
        "data/email_threads.json", EmailThreadJSONSchema
    )
    for email_thread_data in email_threads_data:
        email_thread = EmailThread(**email_thread_data.dict())
        db.session.add(email_thread)
    db.session.commit()
    click.echo(DONE)


def import_email():
    click.echo("Importing Email...", nl=False)
    emails_data = load_and_validate_json("data/emails.json", EmailJSONSchema)
    for email_data in emails_data:
        email = Email(**email_data.dict())
        db.session.add(email)
    db.session.commit()
    click.echo(DONE)
