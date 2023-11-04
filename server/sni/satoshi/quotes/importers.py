from sni.content.importers import JSONImporter
from sni.satoshi.quotes.models import Quote, QuoteCategory, QuoteCategoryFile, QuoteFile
from sni.satoshi.quotes.schemas import QuoteCategoryJSONModel, QuoteJSONModel
from sni.utils.db import get


class QuoteCategoryImporter(JSONImporter):
    filepath = "data/quote_categories.json"
    item_schema = QuoteCategoryJSONModel
    model = QuoteCategory
    file_model = QuoteCategoryFile
    content_type = "quote_categories"


class QuoteImporter(JSONImporter):
    filepath = "data/quotes.json"
    item_schema = QuoteJSONModel
    model = Quote
    file_model = QuoteFile
    content_type = "quotes"

    def process_item_data(self, quote_data):
        quote_data["categories"] = [
            get(QuoteCategory, slug=category)
            for category in quote_data.pop("categories", [])
        ]
        return quote_data
