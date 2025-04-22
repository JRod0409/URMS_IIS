from django.urls import path
from .views import songs_list

urlpatterns = [
    path("", songs_list, name='songs_list')
]