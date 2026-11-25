from flask import Blueprint, request, jsonify

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from core.extensions import db
from models.crop import Crop

crop_bp = Blueprint("crops", __name__)


@crop_bp.route("/", methods=["POST"])
@jwt_required()
def add_crop():

    data = request.get_json(silent=True) or {}

    crop_name = data.get("crop_name", "").strip()

    if not crop_name:

        return jsonify({
            "success": False,
            "message": "Crop name is required."
        }), 400

    if len(crop_name) > 100:

        return jsonify({
            "success": False,
            "message": "Crop name is too long."
        }), 400

    crop = Crop(
        user_id=int(get_jwt_identity()),
        crop_name=crop_name,
        variety=data.get("variety"),
        location=data.get("location"),
        planting_date=data.get("planting_date")
    )

    db.session.add(crop)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Crop added successfully.",
        "crop": crop.to_dict()
    }), 201


@crop_bp.route("/", methods=["GET"])
@jwt_required()
def get_crops():

    user_id = int(get_jwt_identity())

    crops = Crop.query.filter_by(
        user_id=user_id
    ).order_by(Crop.id.desc()).all()

    return jsonify({
        "success": True,
        "count": len(crops),
        "crops": [crop.to_dict() for crop in crops]
    }), 200


@crop_bp.route("/<int:crop_id>", methods=["GET"])
@jwt_required()
def get_crop(crop_id):

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

    return jsonify({
        "success": True,
        "crop": crop.to_dict()
    }), 200


@crop_bp.route("/<int:crop_id>", methods=["DELETE"])
@jwt_required()
def delete_crop(crop_id):

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

    db.session.delete(crop)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Crop deleted successfully."
    }), 200