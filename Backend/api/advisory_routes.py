from flask import Blueprint, jsonify

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from core.extensions import db

from models.crop import Crop, DiseaseDetection

from services.advisory_service import generate_advisory

advisory_bp = Blueprint("advisory", __name__)


@advisory_bp.route("/<int:crop_id>", methods=["GET"])
@jwt_required()
def get_advisory(crop_id):

    user_id = int(get_jwt_identity())

    crop = Crop.query.filter_by(
        id=crop_id,
        user_id=user_id
    ).first()

    if not crop:

        return jsonify({
            "success": False,
            "message": "Crop not found."
        }), 404

    detection = DiseaseDetection.query.filter_by(
        crop_id=crop_id
    ).order_by(
        DiseaseDetection.id.desc()
    ).first()

    if detection:

        disease_name = detection.disease_name
        severity = detection.severity

    else:

        disease_name = "No disease detection available"
        severity = "unknown"

    advisory = generate_advisory(
        crop_name=crop.crop_name,
        disease_name=disease_name,
        severity=severity
    )

    return jsonify({
        "success": True,
        "advisory": advisory
    }), 200