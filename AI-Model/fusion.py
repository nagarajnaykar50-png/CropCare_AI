def fuse(disease_prob, weather):
    score = 0.5 * disease_prob + 0.5 * weather
    if disease_prob > 0.8:  stage = "Infection confirmed"
    elif score > 0.6:       stage = "Early risk - preventive spray karo"
    elif score > 0.4:       stage = "Watch - monitor karo"
    else:                   stage = "Healthy"
    return score, stage