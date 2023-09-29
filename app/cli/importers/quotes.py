import click

from app import db
from app.cli.utils import DONE, get, load_and_validate_json
from app.models import Quote, QuoteCategory
from app.satoshi.quotes.schemas import QuoteCategoryJSONSchema, QuoteJSONSchema


def import_quote_category():
    click.echo("Importing QuoteCategory...", nl=False)
    quote_categories_data = load_and_validate_json(
        "data/quote_categories.json", QuoteCategoryJSONSchema
    )
    for quote_category_data in quote_categories_data:
        quote_category = QuoteCategory(**quote_category_data.dict())
        db.session.add(quote_category)
    db.session.commit()
    click.echo(DONE)


def import_quote():
    click.echo("Importing Quote...", nl=False)
    quotes_data = load_and_validate_json("data/quotes.json", QuoteJSONSchema)
    for _quote_data in quotes_data:
        quote_data = _quote_data.dict()
        quote_data["categories"] = [
            get(QuoteCategory, slug=category)
            for category in quote_data.pop("categories", [])
        ]
        quote = Quote(**quote_data)
        db.session.add(quote)
    db.session.commit()
    click.echo(DONE)
