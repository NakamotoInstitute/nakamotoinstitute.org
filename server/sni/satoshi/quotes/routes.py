from typing import List

from flask import Blueprint, jsonify

from sni.extensions import db
from sni.satoshi.quotes.models import QuoteCategory
from sni.utils.decorators import response_model

from .schemas import QuoteCategoryBaseModel, QuoteCategoryModel

blueprint = Blueprint("quotes", __name__, url_prefix="/quotes")


@blueprint.route("/", methods=["GET"])
@response_model(List[QuoteCategoryBaseModel])
def get_quote_categories():
    categories = db.session.scalars(
        db.select(QuoteCategory).order_by(QuoteCategory.slug)
    ).all()
    return categories


@blueprint.route("/<string:slug>", methods=["GET"])
def get_quote_category(slug):
    category = db.first_or_404(db.select(QuoteCategory).filter_by(slug=slug))
    quotes = category.quotes

    response_data = QuoteCategoryModel(category=category, quotes=quotes)

    return jsonify(response_data.dict(by_alias=True))
