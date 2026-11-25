
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv(
        "SECRET_KEY", "development-secret-change-before-deployment"
    )

    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY", "development-jwt-secret-change-before-deployment"
    )

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///" + os.path.join(BASE_DIR, "cropcare.db")
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAX_CONTENT_LENGTH = 5 * 1024 * 1024

    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
