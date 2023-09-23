from app.cli.data import bp as data_bp


def register(app):
    app.register_blueprint(data_bp)
