from django.urls import path
from .views import HomePage, NewHomePage, LogInPage, SignUpPage, ProfilePage, EditProfilePage

urlpatterns = [
path('home/', NewHomePage, name="home"),
path('', NewHomePage, name="home"),

path('login/', LogInPage, name="login"),
path('signup/', SignUpPage, name="signup"),
path('profile/', ProfilePage, name="profile"),
path('edit/', EditProfilePage, name="edit"),
]