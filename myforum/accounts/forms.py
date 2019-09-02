
import logging
from django import forms

from django.contrib import messages
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget
from django.contrib.auth.models import User
from django.conf import settings
from .models import Profile
from . import auth, util


logger = logging.getLogger("engine")



class SignUpForm(forms.Form):

    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
        max_length=254,
        min_length=2,
    )

    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput,
        strip=False,
        help_text="Enter the same password as before, for verification.",
    )

    email = forms.CharField(
        label="Email",
        strip=False,
        widget=forms.TextInput,
        max_length=254,
        min_length=2,
    )

    def clean_password2(self):

        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords given do not match.")
        return password2

    def clean_email(self):

        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("This email is already being used.")
        return data

    def save(self):

        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password1')
        name = email.split("@")[0]
        user = User.objects.create(email=email, first_name=name)
        user.set_password(password)

        # Send
        auth.send_verification_email(user=user)
        logger.info(f"Signed up user.id={user.id}, user.email={user.email}")

        return user


class SignUpWithCaptcha(SignUpForm):

    def __init__(self, *args, **kwargs):
        super(SignUpWithCaptcha, self).__init__(*args, **kwargs)

        if settings.RECAPTCHA_PRIVATE_KEY:
            self.fields["captcha"] = ReCaptchaField(widget=ReCaptchaWidget())


class LogoutForm(forms.Form):
    pass


class EditProfile(forms.Form):
    email = forms.CharField(label='Email', max_length=100)
    name = forms.CharField(label='Name', max_length=100)
    username = forms.CharField(label="Handler", max_length=100)
    location = forms.CharField(label="Location", max_length=100, required=False)
    website = forms.URLField(label="Website", max_length=225, required=False)
    twitter = forms.CharField(label="Twitter Id", max_length=100, required=False)
    scholar = forms.CharField(label="Scholar", max_length=100, required=False)
    text = forms.CharField(widget=forms.Textarea(),min_length=2, max_length=5000, required=False,
                           help_text="Extra information about you to personalize your profile.")

    message_prefs = forms.ChoiceField(required=True, label="Notifications", choices=Profile.MESSAGING_TYPE_CHOICES,
                                      widget=forms.Select(attrs={'class': "ui dropdown"}),
                                      help_text="""Default mode sends notifications using local messages.""")

    def __init__(self, user,  *args, **kwargs):

        self.user = user

        super(EditProfile, self).__init__(*args, **kwargs)


    def clean_email(self):

        data = self.cleaned_data['email']
        email = User.objects.exclude(pk=self.user.pk).filter(email=data)

        if email.exists():
            raise forms.ValidationError("This email is already being used.")

        return data

    def clean_username(self):

        data = self.cleaned_data['username']
        username = User.objects.exclude(pk=self.user.pk).filter(username=data)

        if len(data.split()) > 1:
            raise forms.ValidationError("No spaces allowed in username/handlers.")
        if username.exists():
            raise forms.ValidationError("This handler is already being used.")

        return data


class LoginForm(forms.Form):

    email = forms.CharField(label='Email', max_length=100)
    password = forms.CharField(label='Password', max_length=100,
                               widget=forms.PasswordInput)


class UserModerate(forms.Form):

    CHOICES = [
        (Profile.NEW, "Reinstate as new user"),
        (Profile.TRUSTED, "Reinstate as trusted user"),
        (Profile.BANNED, "Ban user"),
        (Profile.SUSPENDED, "Suspend user")
    ]

    action = forms.IntegerField(widget=forms.RadioSelect(choices=CHOICES), label="Select Action")

    def __init__(self, source, target, request, *args, **kwargs):
        self.source = source
        self.target = target
        self.request = request
        super(UserModerate, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(UserModerate, self).clean()
        action = cleaned_data['action']
        if not self.source.profile.is_moderator:
            forms.ValidationError("You need to be a moderator to perform that action")

        if action == Profile.BANNED and not self.source.is_superuser:
            raise forms.ValidationError("You need to be an admin to ban users.")

        if self.target.profile.is_moderator and not self.source.is_superuser:
            raise forms.ValidationError("You need to be an admin to moderator moderators.")

        if self.target == self.source:
            raise forms.ValidationError("You can not moderate yourself.")

