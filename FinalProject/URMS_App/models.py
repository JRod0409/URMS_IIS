from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from PIL import Image


class User(models.Model):
    username = models.CharField(max_length=32)
    email = models.CharField(max_length=254)
    isActive = models.BooleanField()
    password = models.CharField(max_length=64, editable=False)

    #I could not seem to get these to upload via the website.
    #profilePic = models.ImageField(upload_to="profile_pictures/", default="profile_pictures/default.png", blank=True)


    def SetPassword(self, newPassword):
        self.password = make_password(newPassword)

    def VerifyPassword(self, attempt):
        return check_password(attempt, self.password)
    

    def RequestSong(self, string):
        return


    def __str__(self):
        returnStatement = "Username: " + str(self.username)
        return str(returnStatement)
    
    def initialSave(self, *args, **kwargs):

        self.isActive = True

        #If no password was given, use "123456"
        if self.password == "":
            self.SetPassword("123456")

        if not self.pk:
            super().save(*args, **kwargs)


class UploadedImage(models.Model):
    image = models.ImageField(upload_to="uploads/")  # Path inside MEDIA_ROOT

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original file first

        # 🔹 Resize Image
        img_path = self.image.path
        max_size = (300, 300)  # Change to desired dimensions

        with Image.open(img_path) as img:
            img.thumbnail(max_size)  # Resize while maintaining aspect ratio
            img.save(img_path)  # Overwrite with resized image
    

#Testing because nothing is showing up :(
class TestModel(models.Model):
    string = models.CharField(max_length=32)

    def __str__(self):
        return self.string
    

class Admin(User):

    def GetUser():
        return "Feature not yet implemented."
    

    def SetUserActive(id):
        return "Feature not yet implemented."


    def SetSong():
        return "Feature not yet implemented."


    def __str__(self):
        return "ADMIN USER - ID:" + str(self.userID) + ", Username: " + str(self.username)
    

class Song(models.Model):
    title = models.CharField(max_length=127)
    album = models.CharField(max_length=127)
    releaseDate = models.DateField()
    dateAdded = models.DateField()
    currentRating = models.DecimalField(decimal_places=1, max_digits=2)
    totalVotes = models.IntegerField()


    def RateSong(self, rating):
        return "Feature not yet implemented."


    def __str__(self):
        return self.title + " - " + str(self.album) + " Rateing: " + str(self.currentRating)