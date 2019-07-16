from django.db import models


class Image(models.Model):
    content = models.TextField()
    origin_url = models.TextField()

    def __str__(self):
        return f'{self.id} - {self.origin_url}'
