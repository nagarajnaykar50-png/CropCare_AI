

def generate_advisory(
    crop_name,
    disease_name,
    severity="unknown",
    weather=None
):

    recommendations = []

    if "demo prediction" in disease_name.lower():

        recommendations.append(
            "Upload an image to a connected AI model "
            "for an actual disease assessment."
        )

    else:

        recommendations.append(
            "Inspect the affected plants and compare "
            "symptoms with reliable agricultural guidance."
        )

    recommendations.extend([
        "Monitor crop health regularly.",
        "Keep the field and farming equipment clean.",
        "Avoid unnecessary watering.",
        "Seek advice from a local agricultural expert "
        "before choosing any treatment."
    ])

    weather_advice = []

    if weather and weather.get("success"):

        humidity = weather.get("humidity")

        if humidity is not None and humidity >= 80:

            weather_advice.append(
                "High humidity is reported. Monitor crops "
                "for moisture-related disease conditions."
            )

    return {
        "crop_name": crop_name,
        "disease_name": disease_name,
        "severity": severity,
        "recommendations": recommendations,
        "weather_advice": weather_advice,
        "disclaimer": (
            "General educational guidance only. "
            "Confirm disease and treatment decisions "
            "with an agricultural specialist."
        )
    }