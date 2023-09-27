import click

from app import db
from app.cli.utils import DONE, load_and_validate_json
from app.models import Translator
from app.translators.schemas import TranslatorMDSchema


def import_translator():
    click.echo("Importing Translator...", nl=False)
    translators_data = load_and_validate_json(
        "data/translators.json", TranslatorMDSchema
    )
    for translator_data in translators_data:
        translator = Translator(**translator_data.dict())
        db.session.add(translator)
    db.session.commit()
    click.echo(DONE)
