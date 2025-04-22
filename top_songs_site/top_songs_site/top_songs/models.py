from django.db import models

class Artists(models.Model):
    name=models.CharField(max_length=32)
    birthplace=models.CharField(max_length=64)
    artist_fact=models.TextField()
    spouse=models.CharField(max_length=32)

    def __str__(self):
        return self.name
    
class Songs(models.Model):
    song_title=models.CharField(max_length=32)
    genre=models.CharField(max_length=32)
    release_year=models.IntegerField()
    score=models.DecimalField(decimal_places=1, max_digits=2)
    artist = models.ForeignKey(Artists, on_delete=models.CASCADE, null=True, blank=True)  # Link to Artists model

    def __str__(self):
        return f"{self.song_title} - {self.artist.name}"