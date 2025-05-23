"""
URL configuration for FinalProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    #Both route to home page
    path('home/', include('URMS_App.urls')),
    path('', include('URMS_App.urls')),

    path('login/', include('URMS_App.urls')),
    path('profile/', include('URMS_App.urls')),
    path('signup/', include('URMS_App.urls')),
    path('edit/', include('URMS_App.urls')),
    path('browse/', include('URMS_App.urls')),
]
