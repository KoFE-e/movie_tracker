from math import ceil

from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect
import requests
from .forms import UserRegistrationForm, LoginForm
from .models import Film, WatchedFilm, WantedFilm
from movie_tracker.settings import KINOPOISK_LINK, KINOPOISK_HEADERS, KINOPOISK_QUERY
# Create your views here.


def index(request):

    wanted_films = WantedFilm.objects.all()
    watched_films = WatchedFilm.objects.all()

    return render(
        request,
        'index.html',
        context={'wanted_films': wanted_films, 'watched_films': watched_films},
    )


def film_detail(request, pk):

    film = Film.objects.get(pk=pk)
    user = request.user
    is_wanted = WantedFilm.objects.filter(filmId=film).filter(userId=user).exists()
    is_watched = WatchedFilm.objects.filter(filmId=film).filter(userId=user).exists()

    return render(
        request,
        'single.html',
        context={'film': film, 'is_wanted': is_wanted, 'is_watched': is_watched},
    )


def change_wanted(request, pk):

    film = Film.objects.get(pk=pk)
    user = request.user
    if WantedFilm.objects.filter(filmId=film).filter(userId=user).exists():
        WantedFilm.objects.filter(filmId=film).filter(userId=user).delete()
    else:
        new_film = WantedFilm(filmId=film, userId=user)
        new_film.save()
    return redirect('film_detail', pk)


def change_watched(request, pk):

    film = Film.objects.get(pk=pk)
    user = request.user
    if WatchedFilm.objects.filter(filmId=film).filter(userId=user).exists():
        WatchedFilm.objects.filter(filmId=film).filter(userId=user).delete()
    else:
        new_film = WatchedFilm(filmId=film, userId=user)
        WantedFilm.objects.filter(filmId=film).filter(userId=user).delete()
        new_film.save()
    return redirect('film_detail', pk)


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password1'])
            # Save the User object
            new_user.save()
            return render(request, 'registration/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/registration.html', {'user_form': user_form})


def signin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.login(request)
            if user:
                login(request, user)
                return redirect('index')
            else:
                return render(request, 'registration/login.html', {'login_form': form})

    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'login_form': form})


def search(request):

    query = KINOPOISK_QUERY
    query['names.name'] = request.GET.get("search")
    response = requests.request("GET", KINOPOISK_LINK, headers=KINOPOISK_HEADERS, params=query)
    res1 = response.json()
    search_results = []
    print(res1)

    for i in range(len(res1['docs'])):
        id = res1['docs'][i]['id']
        title = res1['docs'][i]['names'][0]['name']
        enTitle = res1['docs'][i]['alternativeName']
        if title is None and enTitle is not None:
            title = enTitle
        if enTitle is None:
            enTitle = 'Нет названия'
        descr = res1['docs'][i]['description']
        if descr is None:
            descr = 'Нет описания'
        shortDescr = res1['docs'][i]['shortDescription']
        if shortDescr is None:
            shortDescr = 'Нет краткого описания'
        try:
            image = res1['docs'][i]['poster']['url']
            if image is None:
                image = 'Нет изображения'
        except:
            image = 'Нет изображения'
        try:
            bg = res1['docs'][i]['backdrop']['url']
            if bg is None:
                bg = 'Нет изображения'
        except:
            bg = 'Нет изображения'
        rating = res1['docs'][i]['rating']['kp']
        if rating is None:
            rating = 0
        genresRes = res1['docs'][i]['genres']
        if len(genresRes) == 0 or genresRes is None:
            genres = 'Неизвестно'
        else:
            genres = []
            for genre in genresRes:
                genres.append(genre['name'])
            genres = ', '.join(genres)
        year = res1['docs'][i]['year']
        if year is None:
            year = 0
        type = res1['docs'][i]['type']
        if type is None:
            type = 'Неизвестно'
        if type.find('series') == -1 and type != 'Неизвестно':
            lengthOfMovie = res1['docs'][i]['movieLength']
            if lengthOfMovie is None:
                lengthOfMovie = 0
        else:
            try:
                lengthOfMovie = res1['docs'][i]['seriesLength']
                if lengthOfMovie is None:
                    lengthOfMovie = 0
            except:
                lengthOfMovie = 0
        countriesRes = res1['docs'][i]['countries']
        if len(countriesRes) == 0 or countriesRes is None:
            countries = 'Неизвестно'
        else:
            countries = []
            for country in countriesRes:
                countries.append(country['name'])
            countries = ', '.join(countries)
        try:
            trailer = res1['docs'][i]['videos']['trailers'][0]['url']
            if trailer is None:
                trailer = 'Нет ссылки'
        except:
            trailer = 'Нет ссылки'

        film = Film(kpID=id, title=title, enTitle=enTitle, descr=descr, shortDescr=shortDescr,
                    image=image, bgImage=bg, rating=rating, genres=genres, year=year, typeOfFilm=type,
                    lengthOfMovie=lengthOfMovie, countries=countries, trailerUrl=trailer)
        search_results.append(film)
        if not Film.objects.filter(kpID=id).exists():
            film.save()
    pages = ceil(len(search_results) / 6)
    return render(
        request,
        'search.html',
        context={'search_results': search_results, 'pages': range(pages)},
    )