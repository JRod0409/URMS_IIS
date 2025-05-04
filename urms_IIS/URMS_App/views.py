from django.http import HttpResponse
from django.shortcuts import render, loader, redirect
from django.urls import reverse
from datetime import datetime, timedelta, date
from .models import User,Admin,Song,Artists, Rating
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from random import sample
from django import forms
import re
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from django.conf import settings
from .forms import SpotifySongForm
import base64, requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required

#from .forms import ImageUploadForm

def NewHomePage(request):
    if request.path == "/":
        return redirect("/home/")
    
    if "home" in request.POST:
        return redirect("/home/")
        
    if "profile" in request.POST:
        if request.session.get("loggedUser"):
            username = request.session.get("loggedUser")
            userModel = User.objects.get(username=username)
            return redirect(f"/profile/?user={userModel.username}")
        else:
            return redirect("/login/")

    if "signup" in request.POST:
        return redirect("/signup/")

    if "browse" in request.POST:
        return redirect("/browse/")  
    
    if "logout" in request.POST:
            request.session["loggedUser"] = ""
            return redirect("/home/")
    
    if "login" in request.POST:
            return redirect("/login/")

    userLogedIn = False
    if request.session.get("loggedUser"):
        userLogedIn = True

    # Song Sorting
    sort_by = request.GET.get('sort', 'title')
    valid_sorts = {
        'artist': 'artist__name',
        'genre': 'genre',
        'currentRating': '-currentRating',
        'releaseDate': 'releaseDate'
    }
    sort_field = valid_sorts.get(sort_by, 'title')

    songs = Song.objects.all().order_by(sort_field)

    # ✅ Fixing Lineup Songs
    lineup_songs = sample(list(songs), 5)  # Randomly pick 10 songs from the list

    # Top song and artists
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday())
    top_song = Song.objects.filter(dateAdded__gte=start_of_week).order_by('-currentRating').first()

    if not top_song:
        top_song = Song.objects.order_by('-currentRating').first()

    top_artist_ids = (
        Song.objects.filter(dateAdded__gte=start_of_week)
        .values('artist')
        .annotate(avg_rating=Avg('currentRating'))
        .order_by('-avg_rating')
        .values_list('artist', flat=True)[:3]
    )
    top_artists = Artists.objects.filter(id__in=top_artist_ids)

    template = loader.get_template("homepage.html")
    context = {
        "userLogedIn": userLogedIn,
        "song": songs,
        "lineup_songs": lineup_songs,   # ✅ pass properly
        "current_sort": sort_by,
        "top_song": top_song,
        "top_artists": top_artists,
    }
    
    return HttpResponse(template.render(context, request))





def LogInPage(request):
    
    userLogedIn = False
    error = ""

    if request.session.get("loggedUser"):
        userLogedIn = True

    if request.method == "POST":

        if "home" in request.POST:
            return redirect("/home/")
        
        if "profile" in request.POST:
            if userLogedIn:
                username = request.session.get("loggedUser")
                userModel = User.objects.get(username=username)
                return redirect(f"/profile/?user={userModel.username}")
            
            else:
                return redirect("/login/")

        #If signup button is pushed
        if "signup" in request.POST:
            return redirect("/signup/")

        if "browse" in request.POST:
            return redirect("/browse/")  


        username = request.POST.get("username")
        password = request.POST.get("password")

        #returns the first user that has the name provided
        user = User.objects.filter(username=username).first()

        if user and user.VerifyPassword(password):
            request.session["loggedUser"] = user.username
            return redirect(f"/profile/?user={user.username}")
        
        if username or password:
            error = "Username or Password is incorrect."

    template = loader.get_template("login.html")
    userModel = User.objects.all()
    context = {"users":userModel, "error":error}
    return HttpResponse(template.render(context, request))



def SignUpPage(request):

    error = ""

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        reEnter = request.POST.get("re-enter")

        #check if passwords match
        if not password == reEnter:
            error = "Passwords do not match."

        #check if username is taken
        if User.objects.filter(username=username):
            error = "Username already exists."

        #If there are no errors, proceed
        if "signup" in request.POST and error == "":

            user = User(username=username, email=email, isActive=True)
            user.SetPassword(password)
            user.initialSave()

            return redirect("login")

        if "browse" in request.POST:
            return redirect("/browse/")
        

    template = loader.get_template("signup.html")
    userModel = User.objects.all()
    context = {"users":userModel, "error":error}
    return HttpResponse(template.render(context, request))



def EditProfilePage(request):

    userLogedIn = False

    if request.path == "/":
        return redirect("/home/")

    if request.session.get("loggedUser"):
        userLogedIn = True

    username = request.session.get("loggedUser")
    userModel = User.objects.get(username=username)

    #If user does not have a session ID, send them to login view
    if username == False or userModel == False:
        return redirect("login")

    username = userModel.username

    error = ""

    if request.method == "POST":

        if "home" in request.POST:
            return redirect("/home/")
        
        if "login" in request.POST:
            return redirect("/login/")
        
        if "profile" in request.POST:
            return redirect(f"/profile/?user={username}")
        
        if "logout" in request.POST:
            request.session["loggedUser"] = ""
            return redirect("/home/")

        if "browse" in request.POST:
            return redirect("/browse/")

        if "saveprofile" in request.POST:
            newEmail = request.POST.get("email")

            if userModel.email != newEmail:
                userModel.email = newEmail
                userModel.save()

            return redirect(f"/profile/?user={userModel.username}")

        
    template = loader.get_template("editprofile.html")
    context = {"username":userModel.username, "userEmail":userModel.email, "userModel":userModel, "error":error, "userLogedIn": userLogedIn,}
    return HttpResponse(template.render(context, request))



def ProfilePage(request):

    userLogedIn = False

    if request.path == "/":
        return redirect("/home/")

    if request.session.get("loggedUser"):
        userLogedIn = True

    username = request.session.get("loggedUser")
    userModel = User.objects.get(username=username)

    #If user does not have a session ID, send them to login view
    if username == False:
        return redirect("login")

    username = userModel.username
    userEmail = userModel.email

    if request.method == "POST":

        if "home" in request.POST:
            return redirect("/home/")
        
        if "login" in request.POST:
            return redirect("/login/")
        
        if "profile" in request.POST:
            return redirect(f"/profile/?user={username}")
        
        if "logout" in request.POST:
            request.session["loggedUser"] = ""
            return redirect("/home/")

        if "editprofile" in request.POST:
            return redirect("edit/?user=" + username)
        
        if "browse" in request.POST:
            return redirect("/browse/")


    template = loader.get_template("profile.html")
    context = {"user": userModel, "userLogedIn": userLogedIn,}
    return HttpResponse(template.render(context, request))



def RateSongPage(request, song_id):
    userLogedIn = False

    if request.path == "/":
        return redirect("/home/")

    if request.session.get("loggedUser"):
        userLogedIn = True

    username = request.session.get("loggedUser")
    if not username:
        return redirect("/login/")
    
    if "browse" in request.POST:
        return redirect("/browse/")
    
    if "profile" in request.POST:
        return redirect("/profile/")
    
    if "logout" in request.POST:
            request.session["loggedUser"] = ""
            return redirect("/home/")
    
    if "login" in request.POST:
            return redirect("/login/")
    
    user = User.objects.get(username=username)
    song = get_object_or_404(Song, id=song_id)

    if request.method == "POST":
        rating = request.POST.get('rating')
        if rating:
            rating = float(rating)
            song.totalVotes += 1
            song.currentRating = ((song.currentRating * (song.totalVotes - 1)) + rating) / song.totalVotes
            song.save()

            # 🛠️ Save the Rating
            Rating.objects.create(user=user, song=song, score=rating)

            return redirect("/home/")

    template = loader.get_template("rate_song.html")
    context = {
        "song": song,
        "username": username,
        'spotify_url': song.spotify_url,
        "userLogedIn": userLogedIn,
    }
    return HttpResponse(template.render(context, request))

def Browse(request):
    userLogedIn = False

    if request.path == "/":
        return redirect("/home/")

    if request.session.get("loggedUser"):
        userLogedIn = True

    if request.method == "POST":
        if "logout" in request.POST:
            request.session["loggedUser"] = ""
            return redirect("/home/")
        
        if "profile" in request.POST:
            if userLogedIn:
                username = request.session.get("loggedUser")
                userModel = User.objects.get(username=username)
                return redirect(f"/profile/?user={userModel.username}")
            else:
                return redirect("/login/")
        
        if "login" in request.POST:
            return redirect("/login/")
        
        if "browse" in request.POST:
            return redirect("/browse/")
        
        if "home" in request.POST:
            return redirect("/home/")

    sort_by = request.GET.get('sort', 'title')  # Default sort by title
    valid_sorts = {
        'artist': 'artist__name',
        'genre': 'genre',
        'currentRating': '-currentRating',  
        'releaseDate': 'releaseDate'
    }
    sort_field = valid_sorts.get(sort_by, 'title')

    songs = Song.objects.all().order_by(sort_field)

    # 🛠️ New: fetch top song like in HomePage
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday())
    top_song = Song.objects.filter(dateAdded__gte=start_of_week).order_by('-currentRating').first()

    template = loader.get_template("browse.html")
    context = {
        "userLogedIn": userLogedIn,
        "song": songs,
        "current_sort": sort_by,
        "top_song": top_song,  # 🛠️ Pass top_song to template
    }
    return HttpResponse(template.render(context, request))

def extract_track_id(url):
    match = re.search(r'track/([a-zA-Z0-9]+)', url)
    return match.group(1) if match else None


def get_spotify_token():
    SPOTIFY_CLIENT_ID = '68b3c187a7cc421dbb044c38fa33e85e'
    SPOTIFY_CLIENT_SECRET = '8ea2a36f0665482aa2f1a109cf2d3948'
    auth_str = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}"
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()

    headers = {
        "Authorization": f"Basic {b64_auth_str}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "client_credentials"
    }

    response = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)
    response_data = response.json()
    return response_data.get("access_token")

def AddSongPage(request):
    userLogedIn = False
    username = request.session.get("loggedUser")

    # Redirect to login if not logged in
    if not username:
        return redirect("/login/")

    userLogedIn = True

    # Handle nav bar redirects
    if request.method == "POST":
        if "home" in request.POST:
            return redirect("/home/")
        if "login" in request.POST:
            return redirect("/login/")
        if "profile" in request.POST:
            return redirect(f"/profile/?user={username}")
        if "logout" in request.POST:
            request.session["loggedUser"] = ""
            return redirect("/home/")
        if "browse" in request.POST:
            return redirect("/browse/")
        if "saveprofile" in request.POST:
            newEmail = request.POST.get("email")

        # Handle adding song
        spotify_url = request.POST.get("spotify_url")
        if not spotify_url:
            messages.error(request, "Spotify URL is required.")
            return redirect("addsong")

        # Extract Spotify track ID
        try:
            track_id = spotify_url.split("track/")[1].split("?")[0]
        except IndexError:
            messages.error(request, "Invalid Spotify track URL.")
            return redirect("addsong")

        token = get_spotify_token()
        if not token:
            messages.error(request, "Failed to authenticate with Spotify.")
            return redirect("addsong")

        headers = {
            "Authorization": f"Bearer {token}"
        }

        # Fetch track details
        track_response = requests.get(f"https://api.spotify.com/v1/tracks/{track_id}", headers=headers)
        if track_response.status_code != 200:
            messages.error(request, "Error fetching track from Spotify.")
            return redirect("addsong")

        track_data = track_response.json()
        title = track_data["name"]
        album_name = track_data["album"]["name"]
        album_art_url = track_data["album"]["images"][0]["url"] if track_data["album"]["images"] else None
        artist_name = track_data["artists"][0]["name"]

        # Inside your view where you extract release_date:
        release_date_raw = track_data["album"].get("release_date", None)

        # Normalize to YYYY-MM-DD if possible
        release_date = None
        if release_date_raw:
            try:
                # Year only
                if re.match(r"^\d{4}$", release_date_raw):
                    release_date = f"{release_date_raw}-01-01"
                # Year and month
                elif re.match(r"^\d{4}-\d{2}$", release_date_raw):
                    release_date = f"{release_date_raw}-01"
                # Full date
                elif re.match(r"^\d{4}-\d{2}-\d{2}$", release_date_raw):
                    release_date = release_date_raw
                else:
                    release_date = None  # fallback in case of invalid format

                # Parse to datetime.date to ensure it's valid
                release_date = datetime.strptime(release_date, "%Y-%m-%d").date()

            except Exception as e:
                release_date = None

        # Build Spotify embed link
        embed_url = f"https://open.spotify.com/embed/track/{track_id}"

        # Fetch artist genres
        artist_id = track_data["artists"][0]["id"]
        artist_response = requests.get(f"https://api.spotify.com/v1/artists/{artist_id}", headers=headers)

        if artist_response.status_code == 200:
            artist_data = artist_response.json()
            genres = artist_data.get("genres", [])
            genre = genres[0] if genres else None
        else:
            genre = None

        # Ensure the artist exists
        artist, created = Artists.objects.get_or_create(name=artist_name)

        # Check for duplicates
        existing_song = Song.objects.filter(title__iexact=title, artist=artist).first()
        if existing_song:
            messages.warning(request, f"Song '{title}' by {artist_name} already exists in the database.")
            return redirect("addsong")

        # Create song
        Song.objects.create(
            title=title,
            album=album_name,
            artist=artist,
            releaseDate=release_date,
            genre=genre,
            album_art_url=album_art_url,
            spotify_url=embed_url,
        )

        messages.success(request, f"Song '{title}' by {artist_name} added successfully.")
        return redirect("addsong")

    context = {
        "userLogedIn": userLogedIn,
    }
    return render(request, "add_song.html", context)