# Generated by Django 3.2.5 on 2021-07-27 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0001_initial'),
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='files',
            field=models.ManyToManyField(to='media.File', verbose_name='файлы'),
        ),
    ]
