from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from requests import get

def generate_random_img_url(width=640, height=480):
    return f"{settings.DEV_IMAGES_API}/{width}/{height}"

def fetch_random_image(name):
    file = get(generate_random_img_url())
    image = SimpleUploadedFile(f"{name}.jpg", file.content, "image/jpeg")
    return image


