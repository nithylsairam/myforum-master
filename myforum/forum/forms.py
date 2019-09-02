
from pagedown.widgets import PagedownWidget
from django import forms

from django.core.exceptions import ValidationError
from django.conf import settings
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget
from myforum.accounts.models import User
from .models import Post
from myforum.forum import models, auth

from .const import *

# Share logger with models
logger = models.logger

MIN_CHARS = 5
MAX_CONTENT = 15000
MIN_CONTENT = 10


def english_only(text):
    try:
        text.encode('ascii')
    except Exception:
        raise ValidationError('Text may only contain plain text (ASCII) characters')


def valid_title(text):
    "Validates form input for tags"
    text = text.strip()
    if not text:
        raise ValidationError('Please enter a title')

    text = text.replace(" ", '')
    if len(text) < MIN_CHARS:
        raise ValidationError(f'Too short, please add more than {MIN_CHARS} characters.')


def valid_tag(text):
    "Validates form input for tags"

    words = text.split(",")
    if len(words) > 5:
        raise ValidationError('You have too many tags (5 allowed)')


class CaptchaForm(forms.Form):

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(CaptchaForm, self).__init__(*args, **kwargs)

        not_trusted = True #self.user.is_authenticated and (not self.user.profile.trusted)

        # Untrusted users get a recaptcha field
        if settings.RECAPTCHA_PRIVATE_KEY and not_trusted:
            self.fields["captcha"] = ReCaptchaField(widget=ReCaptchaWidget())


class PostLongForm(forms.Form):

    choices = [opt for opt in Post.TYPE_CHOICES]

    choices = filter(lambda opt: (opt[1] in settings.ALLOWED_POST_TYPES) if settings.ALLOWED_POST_TYPES else
                                 (opt[0] in Post.TOP_LEVEL), choices)

    post_type = forms.IntegerField(label="Post Type",
                                   widget=forms.Select(choices=choices, attrs={'class': "ui dropdown"}),
                                   help_text="Select a post type.")
    title = forms.CharField(label="Post Title", max_length=200, min_length=2,
                            validators=[valid_title, english_only],
                            help_text="Enter a descriptive title to promote better answers.")
    tag_val = forms.CharField(label="Post Tags", max_length=50, required=False, validators=[valid_tag],
                              help_text="""
                              Create a new tag by typing a word then adding a comma or press ENTER or SPACE.
                              """,
                              widget=forms.HiddenInput())
    content = forms.CharField(widget=PagedownWidget(template="widgets/pagedown.html"), validators=[english_only],
                              min_length=MIN_CONTENT, max_length=MAX_CONTENT, label="Post Content", strip=False)

    def __init__(self, post=None, user=None, *args, **kwargs):
        self.post = post
        self.user = user
        super(PostLongForm, self).__init__(*args, **kwargs)

        not_trusted = self.user.is_authenticated and (not self.user.profile.trusted)

        # Untrusted users get a recaptcha field
        if settings.RECAPTCHA_PRIVATE_KEY and not_trusted:
            self.fields["captcha"] = ReCaptchaField(widget=ReCaptchaWidget())

    def edit(self):
        """
        Edit an existing post.
        """
        if self.user != self.post.author and not self.user.profile.is_moderator:
            raise forms.ValidationError("Only the author or a moderator can edit a post.")
        data = self.cleaned_data
        self.post.title = data.get('title')
        self.post.content = data.get("content")
        self.post.type = data.get('post_type')
        self.post.tag_val = data.get('tag_val')
        self.post.lastedit_user = self.user
        self.post.save()
        return self.post

    def clean_tag_val(self):
        """
        Take out duplicates
        """
        tag_val = self.cleaned_data["tag_val"] or 'tag1,tag2'
        tags = set(tag_val.split(","))
        return ",".join(tags)

    def clean_content(self):
        content = self.cleaned_data["content"]
        length = len(content.replace(" ", ""))
        if length < MIN_CHARS:
            raise forms.ValidationError(f"Too short, place add more than {MIN_CHARS}")
        return content


class PostShortForm(forms.Form):
    MIN_LEN, MAX_LEN = 10, 10000
    parent_uid = forms.CharField(widget=forms.HiddenInput(), min_length=2, max_length=32)
    content = forms.CharField(widget=PagedownWidget(template="widgets/pagedown.html"),
                              min_length=MIN_LEN, max_length=MAX_LEN)

    def __init__(self, user=None, post=None, recaptcha=True, *args, **kwargs):
        self.user = user
        self.post = post
        super().__init__(*args, **kwargs)
        self.fields['content'].strip = False

        not_trusted = self.user.is_authenticated and (not self.user.profile.trusted)

        # Untrusted users get a recaptcha field
        if recaptcha and settings.RECAPTCHA_PRIVATE_KEY and not_trusted:
            self.fields["captcha"] = ReCaptchaField(widget=ReCaptchaWidget())


class CommentForm(forms.Form):

    post_uid = forms.CharField(widget=forms.HiddenInput(), min_length=2, max_length=5000)
    content = forms.CharField( widget=forms.Textarea,min_length=2, max_length=5000)


def mod_choices(post):
    """
    Return available moderation options for a post.
    """
    choices = [
        (BUMP_POST, "Bump a post"),
        (MOVE_ANSWER, "Move comment to answer."),
        (OPEN_POST, "Open deleted or off topic post"),
        (DELETE, "Delete post")
    ]

    allowed = []

    # Moderation options for top level posts
    allowed += [BUMP_POST] if post.is_toplevel else []

    # Option to open deleted posts
    if post.status in [Post.DELETED, Post.OFFTOPIC]:
        allowed += [OPEN_POST]

    # Option to deleted open posts
    if post.status != Post.DELETED:
        allowed += [DELETE]

    if post.is_comment:
        allowed += [MOVE_ANSWER]

    # Filter the appropriate choices
    choices = filter(lambda action: action[0] in allowed if allowed else True, choices)

    return choices


class PostModForm(forms.Form):

    def __init__(self, post, request, user, *args, **kwargs):
        self.post = post
        self.user = user
        self.request = request

        super(PostModForm, self).__init__(*args, **kwargs)

        choices = mod_choices(post=self.post)

        if self.post.is_toplevel:
            self.fields['dupe'] = forms.CharField(required=False, max_length=200)
            self.fields['comment'] = forms.CharField(required=False, max_length=200)
            self.fields['offtopic'] = forms.CharField(required=False, max_length=200)
        else:
            self.fields['pid'] = forms.CharField(required=False, max_length=200, label="Parent id")

        self.fields['action'] = forms.IntegerField(widget=forms.RadioSelect(choices=choices), required=False)

    def clean_dupe(self):
        dupe = self.cleaned_data.get("dupe")
        dupes = dupe.split(",")[:5]
        dupes = ','.join(dupes)
        return dupes

    def clean(self):
        action = self.cleaned_data.get("action")
        dupes = self.cleaned_data.get("dupe")
        pid = self.cleaned_data.get("pid")
        offtopic = self.cleaned_data.get("offtopic")

        if (action is None) and not (dupes or pid or offtopic):
            raise forms.ValidationError("Select an action.")

        parent = Post.objects.filter(uid=pid).first()
        if not parent and pid:
            raise forms.ValidationError(f"Parent id: {pid} does not exist.")

        if parent and parent.root != self.post.root:
            raise forms.ValidationError(f"Parent does not share the same root.")

        return self.cleaned_data

