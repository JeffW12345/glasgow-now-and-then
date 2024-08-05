from django import template

register = template.Library()

@register.simple_tag
def user_liked_picture(picture_likes, user, picture_id):
    for picture_like in picture_likes:
        if picture_like.user.username == user.username and picture_like.image.id == picture_id:
            return True
    return False

@register.simple_tag
def any_tags_for_picture(tags, picture_id):
    for tag in tags:
        if tag.picture.id == picture_id:
            return True
    return False