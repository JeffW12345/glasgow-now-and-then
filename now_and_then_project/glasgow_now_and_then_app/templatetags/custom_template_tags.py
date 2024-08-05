from django import template

from ..models import PictureLike

register = template.Library()

@register.filter(name='user_liked_picture')
def user_liked_picture(picture_likes, user):
    for picture_like in picture_likes:
        if picture_like.user.username == user.username:
            return True
    return False