# Generated by Django 4.2 on 2023-05-12 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0002_film_shortdescr'),
    ]

    operations = [
        migrations.AddField(
            model_name='film',
            name='trailerUrl',
            field=models.URLField(default=1, verbose_name='Ссылка на трейлер'),
            preserve_default=False,
        ),
    ]