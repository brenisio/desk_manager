def registrar_blueprints(app):
    from .routes.home import HOME
    app.register_blueprint(HOME)

    from .routes.cliente import CLIENTE
    app.register_blueprint(CLIENTE)

    from .routes.mesa import MESA
    app.register_blueprint(MESA)

    from .routes.planos import PLANO
    app.register_blueprint(PLANO)

    from .routes.reserva import RESERVA
    app.register_blueprint(RESERVA)

    from .routes.registros import REGISTROS
    app.register_blueprint(REGISTROS)

    from .error_handler import error_bp
    app.register_blueprint(error_bp)
