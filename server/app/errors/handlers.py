from flask import jsonify

from . import bp


@bp.app_errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not Found", "message": str(error)}), 404


@bp.app_errorhandler(500)
def server_error(error):
    return (
        jsonify({"error": "An unexpected error occurred", "details": str(error)}),
        500,
    )
