from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Used to generate URLs by reversing the URL patterns


class Film(models.Model):

    kpID = models.IntegerField(verbose_name='ID в КиноПоиске', primary_key=True)
    title = models.CharField(max_length=200, verbose_name='Название')
    enTitle = models.CharField(max_length=200, verbose_name='Название на английском')
    descr = models.TextField(max_length=1000, verbose_name='Описание')
    shortDescr = models.TextField(max_length=200, verbose_name='Краткое описание')
    image = models.URLField(max_length=200, verbose_name='Постер')
    bgImage = models.URLField(max_length=200, verbose_name='Задний план')
    rating = models.FloatField(verbose_name='Рейтинг фильма')
    genres = models.CharField(max_length=300, verbose_name='Жанры')
    year = models.IntegerField(verbose_name='Год выпуска')
    typeOfFilm = models.CharField(max_length=200, verbose_name='Тип')
    lengthOfMovie = models.IntegerField(verbose_name='Продолжительность (в минутах)')
    countries = models.CharField(max_length=200, verbose_name='Страна производства')
    trailerUrl = models.URLField(max_length=200, verbose_name='Ссылка на трейлер')

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.title

    def get_absolute_url(self):
        """
        Returns the url to access a particular film instance.
        """
        return reverse('film_detail', args=[str(self.kpID)])

    def get_url_wanted(self):
        """
        Returns the url to access a particular film instance.
        """
        return reverse('change_wanted', args=[str(self.kpID)])

    def get_url_watched(self):
        """
        Returns the url to access a particular film instance.
        """
        return reverse('change_watched', args=[str(self.kpID)])


class WatchedFilm(models.Model):

    filmId = models.ForeignKey('Film', on_delete=models.CASCADE)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)

    def getkpID(self):
        return str(self.filmId.kpID)

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.filmId.title


class WantedFilm(models.Model):

    filmId = models.ForeignKey('Film', on_delete=models.CASCADE)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)

    def getkpID(self):
        return str(self.filmId.kpID)

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.filmId.title

