from babel.dates import format_date

from app.shared import bp


@bp.app_template_filter()
def commafy(d):
    return f"{d:,}"


@bp.app_template_filter()
def dateformat(d, date_format="long", language="en"):
    """Print a date in a given locale."""
    if language == "fa":
        return format_date(d, "short", language)
    return format_date(d, date_format, language)
