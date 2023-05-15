from django.contrib import admin

# Register your models here.

from .models import Film, WatchedFilm, WantedFilm

#admin.site.register(Film)
#admin.site.register(WatchedFilm)
#admin.site.register(WantedFilm)


class FilmAdmin(admin.ModelAdmin):
    list_display = ('title', 'enTitle', 'kpID')


class WatchedFilmAdmin(admin.ModelAdmin):
    list_display = ('filmId', 'getkpID')


class WantedFilmAdmin(admin.ModelAdmin):
    list_display = ('filmId', 'getkpID')


admin.site.register(Film, FilmAdmin)
admin.site.register(WantedFilm, WantedFilmAdmin)
admin.site.register(WatchedFilm, WatchedFilmAdmin)
