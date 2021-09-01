from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=30)
    description = models.TextField(max_length=150, null=True, blank=True)
    uploaded = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images/', blank=True)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        ordering = ['-uploaded']


class UserSavedImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    post = models.ForeignKey(Post, on_delete=models.CASCADE) 
    
    def __str__(self) -> str:
        return self.user.username    