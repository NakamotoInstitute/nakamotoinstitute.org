from flask import Blueprint, jsonify

blueprint = Blueprint("errors", __name__)


@blueprint.app_errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not Found", "message": str(error)}), 404


@blueprint.app_errorhandler(500)
def server_error(error):
    return (
        jsonify({"error": "An unexpected error occurred", "details": str(error)}),
        500,
    )
