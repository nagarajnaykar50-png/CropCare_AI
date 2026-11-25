import cv2, numpy as np

def severity(image):
    bgr = cv2.cvtColor(np.array(image.convert("RGB")), cv2.COLOR_RGB2BGR)
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    leaf = cv2.inRange(hsv, (10, 40, 20), (90, 255, 255))
    bad = cv2.inRange(hsv, (8, 60, 20), (30, 255, 200))
    pct = 100 * (bad > 0).sum() / max((leaf > 0).sum(), 1)
    level = "Low" if pct < 10 else "Medium" if pct < 30 else "High"
    return float(pct), level