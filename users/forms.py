from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

from .models import UserProfile


class SignupForm(forms.Form):
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'First Name'}),
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'Last Name'}),
    )
    country = CountryField(blank=True).formfield(widget=CountrySelectWidget())

    def signup(self, request, user):
        """Called after user is created but before saved to handle additional fields"""
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

        profile = UserProfile(user=user)
        profile.country = self.cleaned_data.get('country', '')
        profile.save()
