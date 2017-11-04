from babel.dates import format_date

from .. import app


@app.template_filter()
def dateformat(d, date_format="long", lang="en"):
    """Print a date in a given locale."""
    return format_date(d, date_format, lang)
