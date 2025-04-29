import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from datetime import datetime
import random
from URMS_App.models import Artists, Song

# Spotify API credentials
SPOTIFY_CLIENT_ID = '68b3c187a7cc421dbb044c38fa33e85e'
SPOTIFY_CLIENT_SECRET = '8ea2a36f0665482aa2f1a109cf2d3948'

# Authenticate
auth_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

# Playlist ID from your link
playlist_id = '3EstfYfgPCZ6CDkune4vmx'

# Fetch first batch
results = sp.playlist_tracks(playlist_id)
tracks = results['items']

# Handle pagination if needed
while results['next']:
    results = sp.next(results)
    tracks.extend(results['items'])

# Go through each song
for item in tracks:
    track = item['track']
    title = track['name']
    album = track['album']['name']
    release_date = track['album']['release_date']  # Example: "2023-04-21" or "2001"
    artists_list = track['artists']

    # Use the first artist (main one)
    artist_name = artists_list[0]['name']

    # Try to find or create artist
    artist_obj, created = Artists.objects.get_or_create(
        name=artist_name,
        defaults={
            "birthplace": "Unknown",          # Placeholder
            "artist_fact": "No facts yet.",    # Placeholder
            "spouse": "Unknown",               # Placeholder
        }
    )

    # Extract album art URL (getting the largest image)
    album_art_url = track['album']['images'][0]['url'] if track['album']['images'] else None

    # Extract Spotify URL for the track
    spotify_url = track['external_urls']['spotify']

    # Handle release date if it's only a year
    if len(release_date) == 4:  # Year-only format (e.g., "2001")
        release_date = f"{release_date}-01-01"  # Use January 1st as the date

    # Create the song
    Song.objects.create(
        title=title,
        album=album,
        artist=artist_obj,
        releaseDate=datetime.strptime(release_date, "%Y-%m-%d").date(),
        dateAdded=datetime.now().date(),
        currentRating=round(random.uniform(3.0, 5.0), 1),  # Random starting rating (3.0 to 5.0)
        totalVotes=0,
        genre="Unknown",  # You can improve this if you want
        album_art_url=album_art_url,  # Store the album art URL
        spotify_url=spotify_url      # Store the Spotify URL
    )

print("🎵 All songs and artists imported successfully!")
