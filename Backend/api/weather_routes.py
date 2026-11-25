from flask import Blueprint, request, jsonify

from flask_jwt_extended import jwt_required

from services.weather_service import get_weather

weather_bp = Blueprint("weather", __name__)


@weather_bp.route("/", methods=["GET"])
@jwt_required()
def weather():

    latitude = request.args.get("latitude", type=float)
    longitude = request.args.get("longitude", type=float)

    if latitude is None or longitude is None:

        return jsonify({
            "success": False,
            "message": "Latitude and longitude are required."
        }), 400

    if not -90 <= latitude <= 90:

        return jsonify({
            "success": False,
            "message": "Invalid latitude."
        }), 400

    if not -180 <= longitude <= 180:

        return jsonify({
            "success": False,
            "message": "Invalid longitude."
        }), 400

    result = get_weather(
        latitude,
        longitude
    )

    status_code = 200 if result.get("success") else 503

    return jsonify(result), status_code