from django.db import models


class File(models.Model):
    file = models.FileField(upload_to='files', verbose_name='файл', null=False, blank=False)
