import os

from flask import Flask, jsonify

from config import Config

from core.extensions import db, jwt, cors

from api import (
    auth_bp,
    crop_bp,
    disease_bp,
    weather_bp,
    advisory_bp
)

# Import models so SQLAlchemy detects all tables
from models import User, Crop, DiseaseDetection


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    # Create upload directory
    os.makedirs(
        app.config["UPLOAD_FOLDER"],
        exist_ok=True
    )

    # Initialize extensions
    db.init_app(app)

    jwt.init_app(app)

    cors.init_app(
        app,
        resources={
            r"/api/*": {
                "origins": [
                    "http://localhost:3000",
                    "http://127.0.0.1:3000",
                    "http://localhost:5173",
                    "http://127.0.0.1:5173"
                ]
            }
        }
    )

    # Register API blueprints
    app.register_blueprint(
        auth_bp,
        url_prefix="/api/auth"
    )

    app.register_blueprint(
        crop_bp,
        url_prefix="/api/crops"
    )

    app.register_blueprint(
        disease_bp,
        url_prefix="/api/disease"
    )

    app.register_blueprint(
        weather_bp,
        url_prefix="/api/weather"
    )

    app.register_blueprint(
        advisory_bp,
        url_prefix="/api/advisory"
    )

    # Home route
    @app.route("/", methods=["GET"])
    def home():

        return jsonify({
            "success": True,
            "project": "CropCare AI",
            "message": "CropCare AI Backend is running.",
            "version": "1.0.0",
            "ai_mode": app.config["AI_MODE"],
            "status": "running"
        }), 200

    # Health check
    @app.route("/api/health", methods=["GET"])
    def health():

        return jsonify({
            "success": True,
            "status": "healthy",
            "database": "configured",
            "ai_mode": app.config["AI_MODE"]
        }), 200

    # Invalid route handler
    @app.errorhandler(404)
    def not_found(error):

        return jsonify({
            "success": False,
            "message": "API endpoint not found."
        }), 404

    # Upload size handler
    @app.errorhandler(413)
    def file_too_large(error):

        return jsonify({
            "success": False,
            "message": "Image exceeds the 5 MB upload limit."
        }), 413

    # JWT error handlers
    @jwt.unauthorized_loader
    def missing_token(reason):

        return jsonify({
            "success": False,
            "message": "Authentication token is required."
        }), 401

    @jwt.invalid_token_loader
    def invalid_token(reason):

        return jsonify({
            "success": False,
            "message": "Invalid authentication token."
        }), 401

    @jwt.expired_token_loader
    def expired_token(jwt_header, jwt_payload):

        return jsonify({
            "success": False,
            "message": "Authentication token has expired."
        }), 401

    # Create database tables
    with app.app_context():

        db.create_all()

        app.logger.info(
            "CropCare AI database initialized."
        )

    return app


app = create_app()


if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=os.getenv("FLASK_DEBUG", "False").lower() == "true"
    )