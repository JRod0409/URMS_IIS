from django.contrib import admin
from .models import User,Admin,Song,TestModel

admin.site.register(User)
admin.site.register(Admin)
admin.site.register(Song)
admin.site.register(TestModel)