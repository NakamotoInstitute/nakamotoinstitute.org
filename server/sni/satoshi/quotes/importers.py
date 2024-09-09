from sni.content.json import import_json_data
from sni.models import Quote, QuoteCategory
from sni.shared.service import get

from .schemas import QuoteCategoriesJSONModel, QuotesJSONModel


def import_quotes(db_session, force: bool = False, force_conditions: list[bool] = []):
    def process_item_data(item_data):
        item_data["categories"] = [
            get(QuoteCategory, db_session=db_session, slug=category)
            for category in item_data.pop("categories", [])
        ]
        return item_data

    return import_json_data(
        db_session,
        model=Quote,
        schema=QuotesJSONModel,
        file_path="data/quotes.json",
        force=force or any(force_conditions),
        process_item=process_item_data,
    )


def import_quote_categories(
    db_session, force: bool = False, force_conditions: list[bool] = []
):
    return import_json_data(
        db_session,
        model=QuoteCategory,
        schema=QuoteCategoriesJSONModel,
        file_path="data/quote_categories.json",
        dependent_models=[Quote],
        force=force or any(force_conditions),
    )
