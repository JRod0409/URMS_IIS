from django.shortcuts import render
from .models import Songs, Artists

def songs_list(request):
    #songs=Songs.objects.all()
    #artists=Artists.objects.all()
    #return render(request, 'songs/songs_list.html', {'songs':songs, 'artists':artists})
    sort_by = request.GET.get('sort', 'song_title')  # Default sort by title

    # Define allowed sorting fields
    valid_sorts = {
        'artist': 'artist__name',
        'genre': 'genre',
        'score': '-score',  # Descending order (highest score first)
        'release_year': '-release_year'  # Descending order (newest first)
    }

    # Get the actual field name for sorting
    sort_field = valid_sorts.get(sort_by, 'song_title')

    # Query the database with sorting
    songs = Songs.objects.all().order_by(sort_field)

    return render(request, 'songs/songs_list.html', {'songs': songs, 'current_sort': sort_by})