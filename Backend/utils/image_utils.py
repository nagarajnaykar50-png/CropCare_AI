from pathlib import Path
from PIL import Image, UnidentifiedImageError


def validate_image(file):

    if not file or not file.filename:

        return False, "No image selected."

    extension = Path(file.filename).suffix.lower()

    allowed = {".jpg", ".jpeg", ".png", ".webp"}

    if extension not in allowed:

        return False, "Only JPG, JPEG, PNG and WEBP images are allowed."

    try:

        file.stream.seek(0)

        image = Image.open(file.stream)

        image.verify()

        file.stream.seek(0)

        return True, "Valid image."

    except (UnidentifiedImageError, OSError, ValueError):

        file.stream.seek(0)

        return False, "The uploaded file is not a valid image."

    finally:

        file.stream.seek(0)