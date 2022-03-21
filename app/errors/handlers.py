import sys

from flask import current_app, render_template

from app.errors import bp


@bp.app_errorhandler(404)
def not_found(error):
    return render_template("errors/404.html"), 404


@bp.app_errorhandler(500)
def internal_error(error):
    current_app.logger.error("Unhandled exception", exc_info=sys.exc_info())
    return render_template("errors/500.html"), 500
