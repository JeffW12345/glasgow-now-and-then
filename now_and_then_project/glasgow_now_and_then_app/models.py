from django.contrib.auth.models import User
from django.db import models
from django.contrib import admin


class Picture(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pictures')

     ERA_CHOICES = [
          ('Present_day', 'Present Day'),
          ('2010-2020', '2010-2020'),
          ('2000-2010', '2000-2010'),
          ('1990s', '1990s'),
          ('1980s', '1980s'),
          ('1970s', '1970s'),
          ('1960s and earlier', '1960s and earlier')
     ]

     user = models.ForeignKey(User, on_delete=models.CASCADE)
     image = models.ImageField(upload_to='shared_pics')
     title = models.CharField(max_length=190, blank=True)
     description = models.CharField(max_length=1000, blank=True)
     era = models.CharField(max_length=100, choices=ERA_CHOICES)

     when_added = models.DateTimeField(auto_now_add=True)

     def has_picture_already_been_liked_by_user(self, usr):
          return PictureLike.objects.filter(user=usr, image=self).exists()
     def likes_count(self):
          return PictureLike.objects.filter(image=self).count()


     def __str__(self):
          return self.title


class Comment(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE)
     image = models.ForeignKey(Picture, on_delete=models.CASCADE, related_name='comments')

     comment_body = models.TextField(max_length=1000)
     active = models.BooleanField(default=True)

     when_added = models.DateTimeField(auto_now_add=True)

     class Meta:
          ordering = ['when_added']

     def __str__(self):
          return f'Comment by {self.user}: {self.comment_body[:30]}...'


class ImageTag(models.Model):
     picture = models.ForeignKey(Picture, on_delete=models.CASCADE, related_name='image_tags')
     tag_label = models.CharField(max_length=50, blank=True)

     when_added = models.DateTimeField(auto_now_add=True)

     def __str__(self):
          return self.tag_label

     class Meta:
          ordering = ['when_added']
          verbose_name_plural = 'Image Tags'


class PictureLike(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE)
     image = models.ForeignKey(Picture, on_delete=models.CASCADE, related_name='picture_likes')

     when_added = models.DateTimeField(auto_now_add=True)

     class Meta:
          unique_together = ('user', 'image')

     def __str__(self):
          return f'{self.user} likes {self.image}'


# Register models with the admin site
admin.site.register(PictureLike)
admin.site.register(ImageTag)
admin.site.register(Picture)
admin.site.register(Comment)
