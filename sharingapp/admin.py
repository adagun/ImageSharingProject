from .models import Post, UserSavedImage
from django.contrib import admin

# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'uploaded', 'user']


admin.site.register(Post, PostAdmin)

admin.site.register(UserSavedImage)