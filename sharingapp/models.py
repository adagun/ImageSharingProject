from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=30)
    description = models.TextField(max_length=500, null=True, blank=True)
    uploaded = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='images/', blank=False)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        ordering = ['-uploaded']

    def is_edited(self):
        time_diff = (self.edited - self.uploaded).total_seconds()
        print(time_diff)
        return time_diff > 60.0


class UserSavedImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    post = models.ForeignKey(Post, on_delete=models.CASCADE) 
    
    def __str__(self) -> str:
        return f"{self.user.username} - {self.post.title}"


class UserFollow(models.Model):  
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    followed_user = models.ForeignKey(User, on_delete=models.CASCADE)  
    
    def __str__(self) -> str:
        return f"{self.user.username} - {self.followed_user.username}"
