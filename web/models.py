from django.db import models


class Image(models.Model):
    LANG_ENG = 'eng'
    LANG_POL = 'pol'
    languages = (
        (LANG_ENG, 'English'),
        (LANG_POL, 'Polish')
    )

    name = models.TextField(default='')
    content = models.TextField(default='')
    encoded_file = models.TextField(default='')
    url = models.TextField(default='')
    language = models.CharField(max_length=5, default=LANG_POL)

    def __str__(self):
        return f'{self.id} - {self.url}'
