from django.db import models

from media.models import File
from posts.models import Post


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='пост', related_name='comments', null=False, blank=False)
    text = models.TextField(verbose_name='текст', null=False, blank=False)
    files = models.ManyToManyField(File, verbose_name='файлы')

    def __str__(self):
        return f'text: {self.text[:15]}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
