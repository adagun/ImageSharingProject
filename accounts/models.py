from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class UserProfilePicture(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/profilePictures/', blank=False, null=False, default="images/profilePictures/default.png")

    def __str__(self):
        return self.user.username + self.image.__str__()
