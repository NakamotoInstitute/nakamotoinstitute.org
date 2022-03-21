from datetime import timedelta
from decimal import Decimal

import click
import requests
from dateutil import parser
from flask import Blueprint

from app import db
from app.cli.utils import DONE, color_text
from app.models import Price, Skeptic

bp = Blueprint("skeptics", __name__)

bp.cli.help = "Update skeptics."

API_URL = "https://community-api.coinmetrics.io/v4/timeseries/asset-metrics?assets=btc&metrics=PriceUSD&frequency=1d&page_size=10000"  # noqa


def update_skeptics():
    click.echo("Updating skeptics...", nl=False)
    skeptics = Skeptic.query.all()
    prices = Price.query.all()
    price_query = db.session.query(Price)

    for skeptic in skeptics:
        date_diff = (prices[-1].date - skeptic.date).days + 1  # Include first day
        filtered_prices = price_query.filter(Price.date >= skeptic.date).all()
        total_btc = Decimal("0")
        for price_data in filtered_prices:
            btc = round(Decimal("1") / Decimal(price_data.price), 8)
            total_btc += btc
        usd_value = round(total_btc * Decimal(prices[-1].price), 2)
        percent_change = round(
            ((Decimal(usd_value) - Decimal(date_diff)) / Decimal(date_diff)) * 100, 2
        )
        skeptic._btc_balance = str(total_btc)
        skeptic._usd_invested = date_diff
        skeptic._usd_value = str(usd_value)
        skeptic._percent_change = str(percent_change)

        db.session.add(skeptic)
    db.session.commit()
    click.echo(DONE)


@bp.cli.command()
def update():
    """Fetch price data and update skeptics."""
    prices = Price.query.all()
    url = API_URL

    if prices:
        latest = prices[-1]
        start_date = latest.date + timedelta(days=1)
        url += f"&start_time={start_date}"

    click.echo("Fetching prices...", nl=False)
    resp = requests.get(url).json()
    series = resp["data"]
    click.echo(DONE)
    click.echo("Importing prices...", nl=False)
    for se in series:
        date = parser.parse(se["time"])
        price = se["PriceUSD"]
        new_price = Price(
            date=date,
            price=price,
        )
        db.session.add(new_price)
    db.session.commit()
    click.echo(DONE)

    update_skeptics()
    click.echo(color_text("Finished updating!"))
