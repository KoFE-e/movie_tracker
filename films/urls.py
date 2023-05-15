from django.urls import path, re_path
from . import views


urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^film/(?P<pk>\d+)$', views.film_detail, name='film_detail'),
    path('register/', views.register, name='register'),
    path('user_login/', views.signin, name='user_login'),
    path('search/', views.search, name='search'),
    re_path(r'^change_wanted/(?P<pk>\d+)$', views.change_wanted, name='change_wanted'),
    re_path(r'^change_watched/(?P<pk>\d+)$', views.change_watched, name='change_watched')
]
