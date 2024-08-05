from django import template
from django.contrib.auth.models import User

from ..models import PictureLike

register = template.Library()

@register.simple_tag
def user_liked_picture(picture_likes, user, picture_id):
    for picture_like in picture_likes:
        if picture_like.user.username == user.username and picture_like.image.id == picture_id:
            return True
    return False