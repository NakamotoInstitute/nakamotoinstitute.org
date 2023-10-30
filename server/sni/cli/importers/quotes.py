from sni.cli.utils import JSONImporter, get
from sni.satoshi.quotes.models import Quote, QuoteCategory, QuoteCategoryFile, QuoteFile
from sni.satoshi.quotes.schemas import QuoteCategoryJSONModel, QuoteJSONModel


class QuoteCategoryImporter(JSONImporter):
    filepath = "data/quote_categories.json"
    item_schema = QuoteCategoryJSONModel
    model = QuoteCategory
    file_model = QuoteCategoryFile
    content_type = "quote_categories"


def import_quote_category():
    importer = QuoteCategoryImporter()
    importer.run_import()


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


def import_quote():
    importer = QuoteImporter()
    importer.run_import()
