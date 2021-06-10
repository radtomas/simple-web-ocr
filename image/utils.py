import errno
import io
import os
from base64 import b64encode, b64decode
from urllib import request

import PIL
from django.conf import settings
from django.core.exceptions import FieldError
from pytesseract import pytesseract

from image.models import Image


class ImageProcess:

    def __init__(self, context, enforce=False):
        self.context = context
        if not self.context.get("url") or not self.context.get("language"):
            raise FieldError("Missing url or language!")
        self.enforce_process = enforce

    def download_image(self):
        with request.urlopen(self.context("url")) as response:
            encoded_data = b64encode(response.read())
            self.context["encoded_file"] = encoded_data.decode()

    def prepare_enviroment(self):
        if not os.path.exists(settings.TESSERACT_DATA_DIR):
            raise FileNotFoundError(
                errno.ENOENT,
                os.strerror(errno.ENOENT),
                settings.TESSERACT_DATA_DIR
            )

        os.environ['TESSDATA_PREFIX'] = f'{settings.TESSERACT_DATA_DIR}'

    def get_text_from_image(self):
        image_string = io.BytesIO(
            b64decode(self.context.get("encoded_file"))
        )
        image = PIL.Image.open(image_string)
        return pytesseract.image_to_string(
            image,
            lang=self.context.get("language")
        )

    def process_image(self):
        self.prepare_enviroment()
        if not self.context.get("encoded_file"):
            self.download_image()
        if not self.context.get("content") or self.enforce_process:
            self.context["content"] = self.get_text_from_image()
        return self.context
