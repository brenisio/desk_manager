def registrar_blueprints(app):
    from .routes.home import HOME
    app.register_blueprint(HOME)

    from .routes.cliente import CLIENTE
    app.register_blueprint(CLIENTE)

