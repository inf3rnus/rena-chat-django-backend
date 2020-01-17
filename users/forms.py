from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields

# There is no model to base this form off of that's included in auth.forms
class CustomUserDetailsForm(forms.Form):
    username = forms.CharField(label='username', max_length=150, required=True)
    bio = forms.CharField(label='bio', max_length=300, required=False)
    profile_picture = forms.ImageField(label='profile_picture', required=False)