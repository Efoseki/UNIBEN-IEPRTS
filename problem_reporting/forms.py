from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class CaseInsensitiveUsernameMixin:
    """Normalise usernames to lower case while leaving passwords unchanged."""

    def clean_username(self):
        username = self.cleaned_data.get('username', '')
        return username.strip().lower()


class CaseInsensitiveUserCreationForm(CaseInsensitiveUsernameMixin, UserCreationForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        label='Username',
        help_text='Usernames are not case-sensitive. For example, John and john are treated as the same username.',
    )

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def clean_username(self):
        username = super().clean_username()
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError(
                'This username is already in use. Usernames are not case-sensitive, so please choose a different username.',
                code='duplicate_username',
            )
        return username


class CaseInsensitiveAuthenticationForm(CaseInsensitiveUsernameMixin, AuthenticationForm):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={'autofocus': True}),
    )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            self.user_cache = authenticate(
                self.request,
                username=username.strip().lower(),
                password=password,
            )
            if self.user_cache is None:
                raise forms.ValidationError(
                    'Invalid username or password. Usernames are not case-sensitive, but passwords are case-sensitive.',
                    code='invalid_login',
                )
            self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data
