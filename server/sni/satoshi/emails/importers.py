from sni.content.json import import_json_data
from sni.models import Email, EmailThread, Quote

from .schemas import EmailsJSONModel, EmailThreadsJSONModel


def import_emails(
    db_session, force: bool = False, force_conditions: list[bool] | None = None
):
    return import_json_data(
        db_session,
        model=Email,
        schema=EmailsJSONModel,
        file_path="data/emails.json",
        force=force or any(force_conditions or []),
    )


def import_email_threads(
    db_session, force: bool = False, force_conditions: list[bool] | None = None
):
    return import_json_data(
        db_session,
        model=EmailThread,
        schema=EmailThreadsJSONModel,
        file_path="data/email_threads.json",
        dependent_models=[Email, Quote],
        force=force or any(force_conditions or []),
    )
