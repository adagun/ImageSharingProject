from django.contrib import admin

# Register your models here.
from django.utils.html import format_html

from accounts.models import UserProfilePicture


# show image in admin panel
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'image_tag', 'id')
    def image_tag(self, obj):
        return format_html('<img src="{0}" style="width:25px; height:25px;" />'.format(obj.image.url))

admin.site.register(UserProfilePicture, ProfileAdmin)
