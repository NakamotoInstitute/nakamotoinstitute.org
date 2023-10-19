import click

from sni.cli.utils import DONE, load_all_markdown_files
from sni.extensions import db
from sni.translators.models import Translator
from sni.translators.schemas import TranslatorMDModel


def import_translator():
    click.echo("Importing Translator...", nl=False)
    translators_data = load_all_markdown_files("content/translators", TranslatorMDModel)
    for translator_data in translators_data:
        translator = Translator(**translator_data)
        db.session.add(translator)
    db.session.commit()
    click.echo(DONE)
