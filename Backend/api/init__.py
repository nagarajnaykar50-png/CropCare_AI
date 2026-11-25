from api.auth_routes import auth_bp
from api.crop_routes import crop_bp
from api.disease_routes import disease_bp
from api.weather_routes import weather_bp
from api.advisory_routes import advisory_bp

__all__ = [
    "auth_bp",
    "crop_bp",
    "disease_bp",
    "weather_bp",
    "advisory_bp"
]