from django import forms
from django.contrib.auth.models import User
from .models import Picture, Comment, ImageTag, PictureLike

ERA_CHOICES = [
    ('Present_day', 'Present Day'),
    ('2010-2020', '2010-2020'),
    ('2000-2010', '2000-2010'),
    ('1990s', '1990s'),
    ('1980s', '1980s'),
    ('1970s', '1970s'),
    ('1960s and earlier', '1960s and earlier')
]

class PictureForm(forms.ModelForm):
    class Meta:
        model = Picture
        fields = ('image', 'title', 'description', 'era')
        widgets = {
            'title': forms.TextInput(attrs={'size': '170'}),
            'description': forms.Textarea(),
            'era': forms.Select(choices=ERA_CHOICES),
        }

class ImageTagForm(forms.ModelForm):
    class Meta:
        model = ImageTag
        fields = ('tag_label',)
        widgets = {
            'tag_label': forms.TextInput(attrs={'size': '170'}),
        }

class CommentForm(forms.ModelForm):
    image_id = forms.IntegerField(widget=forms.HiddenInput())
    user_id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = Comment
        fields = ['comment_body']  # Only include fields that need user input
        widgets = {
            'comment_body': forms.Textarea(attrs={'cols': 80, 'rows': 5}),
        }

class PictureLikeForm(forms.ModelForm):
    image_id = forms.IntegerField(widget=forms.HiddenInput())
    user_id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = PictureLike
        fields = ['image_id', 'user_id']
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'password')