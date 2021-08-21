from flask import redirect, render_template, request, url_for
from sqlalchemy import desc

from app import cache
from app.models import Quote, QuoteCategory
from app.satoshi.quotes import bp


@bp.route("/")
@cache.cached()
def index():
    categories = QuoteCategory.query.order_by(QuoteCategory.slug).all()
    return render_template("satoshi/quotes/index.html", categories=categories)


@bp.route("/<string:slug>/")
@cache.cached()
def detail_category(slug):
    category = QuoteCategory.query.filter_by(slug=slug).first()
    if category is not None:
        order = request.args.get("order")
        quote_query = category.quotes
        if order == "desc":
            quote_query = quote_query.order_by(desc(Quote.date))
        else:
            quote_query = quote_query.order_by(Quote.date)
        quotes = quote_query.all()
        return render_template(
            "satoshi/quotes/detail_category.html",
            quotes=quotes,
            category=category,
            order=order,
        )
    else:
        return redirect(url_for("satoshi.quotes.index"))
