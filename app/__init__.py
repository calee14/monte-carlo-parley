from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "your-secret-key"  # Change this in production

    # Register blueprints
    from app.views.main import main_bp
    from app.views.simulation import simulation_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(simulation_bp)

    return app
