from classifier import predict
from severity import severity
from gradcam import gradcam
from weather import weather_risk
from fusion import fuse

def analyze(image, lat, lon):
    disease, conf, disease_prob = predict(image)
    sev_pct, sev_level = severity(image)
    weather = weather_risk(lat, lon)
    score, stage = fuse(disease_prob, weather)
    return {
        "disease": disease,
        "confidence": conf,
        "severity_pct": sev_pct,
        "severity_level": sev_level,
        "weather_risk": weather,
        "risk_score": score,
        "stage": stage,
        "gradcam_image": gradcam(image),
    }