import click

from sni import db
from sni.cli.utils import DONE, load_and_validate_json
from sni.models import Skeptic
from sni.skeptics.schemas import SkepticJSONModel


def import_skeptic():
    click.echo("Importing Skeptic...", nl=False)
    skeptics_data = load_and_validate_json("data/skeptics.json", SkepticJSONModel)
    for skeptic_data in skeptics_data:
        skeptic = Skeptic(**skeptic_data.dict())
        db.session.add(skeptic)
    db.session.commit()
    click.echo(DONE)
