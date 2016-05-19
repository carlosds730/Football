from django import forms
from django.contrib.auth.models import User
from .models import Player


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    # By convention, all methods named clean_<fieldname> and defined inside a ModelForm are called when is_valid() is called
    def clean_password2(self):
        """
        Validates that the passwords are the same
        :return: The password or raise a Validation Error with message
        """
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

    def clean_username(self):
        """
        Validate that a new user doesn't register with a name that is already in use by another user
        :return: The username or raise a Validation Error with message
        """
        cd = self.cleaned_data
        try:
            player = Player.objects.get(name_excel=cd['username'])
            if player.user:
                raise forms.ValidationError(
                    'There\'s a user already registered with that username. Choose a different one')
            return cd['username']
        except Player.DoesNotExist:
            return cd['username']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class PlayerEditForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ('image',)
