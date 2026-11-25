from pathlib import Path
from uuid import uuid4

from flask import (
    Blueprint,
    request,
    jsonify,
    current_app
)

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from werkzeug.utils import secure_filename

from core.extensions import db
from models.crop import Crop, DiseaseDetection

from services.ai_service import predict_disease
from utils.image_utils import validate_image

disease_bp = Blueprint("disease", __name__)


@disease_bp.route("/detect/<int:crop_id>", methods=["POST"])
@jwt_required()
def detect_disease(crop_id):

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

    if "image" not in request.files:

        return jsonify({
            "success": False,
            "message": "Please upload a crop image."
        }), 400

    image = request.files["image"]

    valid, message = validate_image(image)

    if not valid:

        return jsonify({
            "success": False,
            "message": message
        }), 400

    upload_folder = Path(
        current_app.config["UPLOAD_FOLDER"]
    )

    upload_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    original_name = secure_filename(image.filename)

    extension = Path(original_name).suffix.lower()

    filename = f"{uuid4().hex}{extension}"

    image_path = upload_folder / filename

    try:

        image.save(str(image_path))

        result = predict_disease(
            str(image_path),
            crop.crop_name
        )

        if not result.get("success"):

            image_path.unlink(missing_ok=True)

            return jsonify(result), 503

        detection = DiseaseDetection(
            crop_id=crop.id,
            image_filename=filename,
            disease_name=result["disease_name"],
            severity=result.get("severity"),
            confidence=result.get("confidence"),
            prediction_mode=result.get("mode", "mock")
        )

        db.session.add(detection)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Image processed successfully.",
            "prediction": detection.to_dict(),
            "details": result
        }), 201

    except Exception:

        db.session.rollback()
        image_path.unlink(missing_ok=True)

        current_app.logger.exception(
            "Disease detection failed"
        )

        return jsonify({
            "success": False,
            "message": "Unable to process image."
        }), 500


@disease_bp.route("/history/<int:crop_id>", methods=["GET"])
@jwt_required()
def detection_history(crop_id):

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

    records = DiseaseDetection.query.filter_by(
        crop_id=crop_id
    ).order_by(
        DiseaseDetection.id.desc()
    ).all()

    return jsonify({
        "success": True,
        "count": len(records),
        "history": [
            record.to_dict()
            for record in records
        ]
    }), 200