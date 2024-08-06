from typing import Iterable

from django import template
from django.contrib.auth.models import User

from ..models import PictureLike, ImageTag

register = template.Library()

@register.simple_tag
def user_liked_picture(picture_likes: Iterable[PictureLike], user: User, picture_id: int) -> bool:
    for picture_like in picture_likes:
        if picture_like.user.username == user.username and picture_like.image.id == picture_id:
            return True
    return False

@register.simple_tag
def any_tags_for_picture(tags: Iterable[ImageTag], picture_id: int) -> bool:
    for tag in tags:
        if tag.picture.id == picture_id:
            return True
    return False
