from django.db import models
from django.contrib.auth.models import User

class Artist(models.Model):
    name = models.CharField(max_length=255, unique=True)
    genre = models.CharField(max_length=100)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def average_rating(self):
        ratings = self.ratings.all()
        return ratings.aggregate(models.Avg('score'))['score__avg'] if ratings else None

class Rating(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # Rating from 1 to 5
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('artist', 'user')  # Prevent duplicate ratings

    def __str__(self):
        return f"{self.user.username} rated {self.artist.name}: {self.score}"