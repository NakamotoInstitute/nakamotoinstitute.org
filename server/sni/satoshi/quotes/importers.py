from sni.content.json import JSONImporter
from sni.models import Quote, QuoteCategory, QuoteCategoryFile, QuoteFile
from sni.shared.service import get

from .schemas import QuoteCategoriesJSONModel, QuotesJSONModel


class QuoteImporter(JSONImporter):
    file_path = "data/quotes.json"
    schema = QuotesJSONModel
    model = Quote
    file_model = QuoteFile
    content_type = "quotes"

    def process_item_data(self, quote_data):
        quote_data["categories"] = [
            get(QuoteCategory, db_session=self.db_session, slug=category)
            for category in quote_data.pop("categories", [])
        ]
        return quote_data


class QuoteCategoryImporter(JSONImporter):
    file_path = "data/quote_categories.json"
    schema = QuoteCategoriesJSONModel
    model = QuoteCategory
    file_model = QuoteCategoryFile
    content_type = "quote_categories"
    dependent_importers = [QuoteImporter]
