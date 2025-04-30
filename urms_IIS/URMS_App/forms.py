from django import forms

class SpotifySongForm(forms.Form):
    spotify_url = forms.URLField(label='Spotify Track URL', required=True)
