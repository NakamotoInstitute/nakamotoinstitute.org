from flask import Blueprint

from app.finney.rpow import bp as rpow_bp

bp = Blueprint("finney", __name__, url_prefix="/finney")
bp.register_blueprint(rpow_bp)

from app.finney import routes  # noqa: E402, F401
