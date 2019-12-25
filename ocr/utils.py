import errno
import io
import os
from base64 import b64encode, b64decode
from urllib import request

import PIL
from django.conf import settings
from pytesseract import pytesseract

from web.models import Image


class ImageProcess:

    def __init__(self, url, language, enforce=False):
        if not url or not language:
            raise TypeError

        self.image_instance, created = Image.objects.get_or_create(
            url=url,
            language=language
        )
        self.enforce_process = enforce

    def download_image(self):
        with request.urlopen(self.image_instance.url) as response:
            encoded_data = b64encode(response.read())
            self.image_instance.encoded_file = encoded_data.decode()

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
            b64decode(self.image_instance.encoded_file)
        )
        image = PIL.Image.open(image_string)
        return pytesseract.image_to_string(
            image,
            lang=self.image_instance.language
        )

    def process_image(self):
        self.prepare_enviroment()
        if not self.image_instance.encoded_file:
            self.download_image()
        if not self.image_instance.content or self.enforce_process:
            self.image_instance.content = self.get_text_from_image()
            self.image_instance.save()
        return self.image_instance
