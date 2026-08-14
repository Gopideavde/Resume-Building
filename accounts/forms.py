from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, UserProfile

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    mobile = forms.CharField(max_length=15, required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'first_name', 'last_name', 'mobile')

    def save(self, commit=True):
        user = super().save(commit=False)
        if not user.username:
            user.username = user.email
        if commit:
            user.save()
        return user
        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_photo', 'location', 'linkedin_url', 'github_url', 'website']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'mobile']
