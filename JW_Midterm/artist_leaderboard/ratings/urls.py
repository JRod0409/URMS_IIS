from django.urls import path
from . import views

urlpatterns = [
    path('', views.leaderboard, name='leaderboard'),
    path('rate/', views.rate_artist, name='rate_artist'),
]