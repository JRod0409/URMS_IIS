from django.urls import path
from .views import HomePage, LogInPage, SignUpPage, ProfilePage, EditProfilePage

urlpatterns = [
path('home/', HomePage, name="home"),
path('', HomePage, name="home"),

path('login/', LogInPage, name="login"),
path('signup/', SignUpPage, name="signup"),
path('profile/', ProfilePage, name="profile"),
path('edit/', EditProfilePage, name="edit"),
]