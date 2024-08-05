from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction

from ...models import Picture, Comment, ImageTag, PictureLike


class Command(BaseCommand):
     help = 'Insert initial data into the database'

     @transaction.atomic
     def handle(self, *args, **kwargs):
          # Clear existing data
          self.stdout.write('Clearing existing data...')

          self.delete_old_objects()

          self.stdout.write(self.style.SUCCESS('Successfully cleared existing data'))

          user1, user2 = self.create_users()

          picture1, picture2 = self.create_pictures(user1, user2)

          self.create_comments(picture1, picture2, user1, user2)

          self.create_image_tags(picture1, picture2)

          self.create_likes(picture1, picture2, user1, user2)

          self.stdout.write(self.style.SUCCESS('Successfully inserted initial data'))

     def create_likes(self, picture1, picture2, user1, user2):
          PictureLike.objects.create(user=user1, image=picture2)
          PictureLike.objects.create(user=user2, image=picture1)

     def create_image_tags(self, picture1, picture2):
          ImageTag.objects.create(picture=picture1, tag_label='fireworks')
          ImageTag.objects.create(picture=picture1, tag_label='night')
          ImageTag.objects.create(picture=picture2, tag_label='Glasgow')
          ImageTag.objects.create(picture=picture2, tag_label='Maryhill')

     def create_comments(self, picture1, picture2, user1, user2):
          Comment.objects.create(user=user1, image=picture1, comment_body='Amazing!')
          Comment.objects.create(user=user2, image=picture1, comment_body='Superb!')
          Comment.objects.create(user=user2, image=picture2, comment_body='I love this place!')

     def create_pictures(self, user1, user2):
          picture1 = Picture.objects.create(user=user1, image='shared_pics/fireworks.jpg',
                                            title='Fireworks',
                                            description='Stunning firework display',
                                            era='2010-2020')
          picture2 = Picture.objects.create(user=user2,
                                            image='shared_pics/View-from-kitchen-window-of-Maryhill-tenements.1970.jpg',
                                            title='A view from a kitchen window, Maryhill 1970 something',
                                            description='This takes me back',
                                            era='1970s')
          return picture1, picture2

     def create_users(self):
          user1 = User.objects.create_user(username='john_doe', email='john@example.com', password='password123')
          user2 = User.objects.create_user(username='jane_smith', email='jane@example.com', password='password123')
          return user1, user2

     def delete_old_objects(self):
          PictureLike.objects.all().delete()
          ImageTag.objects.all().delete()
          Comment.objects.all().delete()
          Picture.objects.all().delete()
          User.objects.all().delete()
