import click

from app import db
from app.cli.utils import DONE, load_all_markdown_files
from app.models import Translator
from app.translators.schemas import TranslatorMDModel


def import_translator():
    click.echo("Importing Translator...", nl=False)
    translators_data = load_all_markdown_files("content/translators", TranslatorMDModel)
    for translator_data in translators_data:
        translator = Translator(**translator_data)
        db.session.add(translator)
    db.session.commit()
    click.echo(DONE)
