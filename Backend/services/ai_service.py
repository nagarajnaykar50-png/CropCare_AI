from flask import current_app


def predict_disease(image_path, crop_name):

    ai_mode = current_app.config["AI_MODE"]

    if ai_mode == "mock":

        return {
            "success": True,
            "mode": "mock",
            "crop_name": crop_name,
            "disease_name": "Demo prediction - AI model not connected",
            "severity": "unknown",
            "confidence": None,
            "message": (
                "This is a demonstration response. "
                "No actual disease analysis was performed."
            )
        }

    return {
        "success": False,
        "mode": ai_mode,
        "message": "AI prediction service is not configured."
    }