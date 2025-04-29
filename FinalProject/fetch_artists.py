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
playlist_id = '2hMGNPsSqH4FIhcznuS8cL'

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
    artist_info = artists_list[0]
    artist_name = artist_info['name']
    artist_id = artist_info['id']  # <-- needed to get genres

    # Try to find or create artist
    artist_obj, created = Artists.objects.get_or_create(
        name=artist_name,
        defaults={
            "birthplace": "Unknown",
            "artist_fact": "No facts yet.",
            "spouse": "Unknown",
        }
    )

    # Get album art URL
    album_art_url = track['album']['images'][0]['url'] if track['album']['images'] else None

    # Get Spotify track URL
    spotify_url = track['external_urls']['spotify']

    # Handle release date if only year
    if len(release_date) == 4:
        release_date = f"{release_date}-01-01"

    # 🎸 Get genre by querying the artist info
    genre_list = []
    try:
        artist_data = sp.artist(artist_id)
        genre_list = artist_data.get('genres', [])
    except Exception as e:
        print(f"Couldn't fetch genres for {artist_name}: {e}")

    genre = genre_list[0] if genre_list else "Unknown"

    # 🎵 Build the Spotify embed URL (optional)
    # The normal track URL is like https://open.spotify.com/track/{track_id}
    # Embed URL is like https://open.spotify.com/embed/track/{track_id}
    track_id = track['id']
    spotify_embed_url = f"https://open.spotify.com/embed/track/{track_id}"

    # Create the song
    Song.objects.create(
        title=title,
        album=album,
        artist=artist_obj,
        releaseDate=datetime.strptime(release_date, "%Y-%m-%d").date(),
        dateAdded=datetime.now().date(),
        currentRating=round(random.uniform(3.0, 5.0), 1),
        totalVotes=0,
        genre=genre,
        album_art_url=album_art_url,
        spotify_url=spotify_embed_url  # Use the embed link now
    )

print("🎵 All songs and artists imported successfully with genres and embeds!")
