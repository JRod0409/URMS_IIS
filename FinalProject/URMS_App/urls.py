from django.urls import path
from .views import NewHomePage, LogInPage, SignUpPage, ProfilePage, EditProfilePage, RateSongPage, Browse

urlpatterns = [
path('home/', NewHomePage, name="home"),
path('', NewHomePage, name="home"),

path('login/', LogInPage, name="login"),
path('signup/', SignUpPage, name="signup"),
path('profile/', ProfilePage, name="profile"),
path('edit/', EditProfilePage, name="edit"),
path('rate/<int:song_id>/', RateSongPage, name='rate_song'),
path('browse/', Browse, name='browse'),
]