from sni.content.json import JSONImporter
from sni.models import Email, EmailFile, EmailThread, EmailThreadFile
from sni.satoshi.quotes.importers import QuoteImporter

from .schemas import EmailsJSONModel, EmailThreadsJSONModel


class EmailImporter(JSONImporter):
    file_path = "data/emails.json"
    schema = EmailsJSONModel
    model = Email
    file_model = EmailFile
    content_type = "emails"


class EmailThreadImporter(JSONImporter):
    file_path = "data/email_threads.json"
    schema = EmailThreadsJSONModel
    model = EmailThread
    file_model = EmailThreadFile
    content_type = "email_threads"
    dependent_importers = [QuoteImporter, EmailImporter]
