import click

from app import db
from app.cli.utils import DONE, load_and_validate_json
from app.models import Skeptic
from app.skeptics.schemas import SkepticJSONSchema


def import_skeptic():
    click.echo("Importing Skeptic...", nl=False)
    skeptics_data = load_and_validate_json("data/skeptics.json", SkepticJSONSchema)
    for skeptic_data in skeptics_data:
        skeptic = Skeptic(**skeptic_data.dict())
        db.session.add(skeptic)
    db.session.commit()
    click.echo(DONE)
