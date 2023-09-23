from app.cli.data import bp as data_bp

# from app.cli.skeptics import bp as skeptics_bp


def register(app):
    app.register_blueprint(data_bp)
    # app.register_blueprint(skeptics_bp)
