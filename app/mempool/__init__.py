from flask import Blueprint

from app.mempool.series import bp as series_bp

bp = Blueprint("mempool", __name__, url_prefix="/mempool")
bp.register_blueprint(series_bp)

from app.mempool import routes  # noqa: E402, F401
