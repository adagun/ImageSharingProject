from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from accounts.models import UserProfilePicture


class UserCreationForm(DjangoUserCreationForm):
    first_name = forms.CharField(max_length=255, label="First name", required=True)
    last_name = forms.CharField(max_length=255, label="Last name", required=True)
    email = forms.EmailField(label="Email", required=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "username")

    def clean_email(self):
        email = self.cleaned_data.get("email").lower()
        try:
            user = User.objects.get(email__iexact=email)
            raise forms.ValidationError(
                "A user with that email already exists.")
        except User.DoesNotExist:
            return email


class UserProfilePicForm(ModelForm):
    class Meta:
        model = UserProfilePicture
        fields = ['image']
        widgets = {
            'image': forms.FileInput(),
        }

