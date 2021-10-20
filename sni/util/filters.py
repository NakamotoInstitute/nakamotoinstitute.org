from babel.dates import format_date

from .. import app


@app.template_filter()
def commafy(d):
    """
    """
    return '{d:,}'


@app.template_filter()
def dateformat(d, date_format="long", lang="en"):
    """Print a date in a given locale."""
    if lang == 'fa':
        return format_date(d, "short", lang)
    return format_date(d, date_format, lang)
