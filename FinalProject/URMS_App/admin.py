from django.contrib import admin
from .models import User,Admin,Song,TestModel,Artists

class SongAdmin(admin.ModelAdmin):
    search_fields = ['title', 'album', 'genre', 'album_art_url']

admin.site.register(User)
admin.site.register(Admin)
admin.site.register(Artists)
admin.site.register(Song, SongAdmin)