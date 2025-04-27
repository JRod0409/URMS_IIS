from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from .models import Artist, Rating

def leaderboard(request):
    artists = Artist.objects.all().annotate(avg_rating=Avg('ratings__score')).order_by('-avg_rating')
    return render(request, 'ratings/leaderboard.html', {'artists': artists})

@login_required
def rate_artist(request):
    if request.method == "POST":
        artist_id = request.POST.get("artist")
        score = int(request.POST.get("score"))

        artist = Artist.objects.get(id=artist_id)
        rating, created = Rating.objects.update_or_create(
            artist=artist, user=request.user, defaults={'score': score}
        )

        return redirect("leaderboard")

    artists = Artist.objects.all()
    return render(request, "ratings/rate_artist.html", {"artists": artists})