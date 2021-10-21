#!/usr/bin/env python

from decimal import Decimal

import requests
from datetime import timedelta
from dateutil import parser

from sni import db
from sni.models import Price, Skeptic


def update_skeptics():
    """
    """
    skeptics = Skeptic.query.all()
    prices = Price.query.all()
    price_query = db.session.query(Price)

    for skeptic in skeptics:
        date_diff = (prices[-1].date - skeptic.date).days + 1  # Include first day
        filtered_prices = price_query.filter(Price.date >= skeptic.date).all()
        total_btc = Decimal()
        for price_data in filtered_prices:
            btc = round(Decimal('1') / Decimal(price_data.price), 8)
            total_btc += btc
        usd_value = round(total_btc * Decimal(prices[-1].price), 2)
        percent_change = round(
            ((Decimal(usd_value) - Decimal(date_diff)) / Decimal(date_diff)) * 100, 2)
        skeptic._btc_balance = str(total_btc)
        skeptic._usd_invested = date_diff
        skeptic._usd_value = str(usd_value)
        skeptic._percent_change = str(percent_change)

        db.session.add(skeptic)
    db.session.commit()


def main():
    """
    """
    url = 'https://community-api.coinmetrics.io/v2/assets/btc/metricdata?metrics=PriceUSD'
    prices = Price.query.all()

    if prices:
        latest = prices[-1]
        latest.date + timedelta(days=1)
        url = '{url}&start={start_date}'

    resp = requests.get(url).json()
    series = resp['metricData']['series']
    for se in series:
        date = parser.parse(se['time'])
        price = se['values'][0]
        new_price = Price(
            date=date,
            price=price,
        )
        db.session.add(new_price)
        db.session.commit()

    update_skeptics()


if __name__ == "__main__":
    main()
