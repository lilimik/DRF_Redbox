from django.db import models

from media.models import File
from posts.managers import PostManager


class Post(models.Model):
    objects = PostManager()
    name = models.CharField(max_length=250, verbose_name='Название', null=False, blank=False)
    content = models.TextField(verbose_name='контент', null=False, blank=False)
    files = models.ManyToManyField(File, verbose_name='файлы')

    def __str__(self):
        return f'name: {self.name[:15]}, content: {self.content[:15]}'

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
