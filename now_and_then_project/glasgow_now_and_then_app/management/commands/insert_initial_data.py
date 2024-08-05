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

          # Clear PictureLikes
          PictureLike.objects.all().delete()

          # Clear ImageTags
          ImageTag.objects.all().delete()

          # Clear Comments
          Comment.objects.all().delete()

          # Clear Pictures
          Picture.objects.all().delete()

          # Clear Users
          User.objects.all().delete()

          self.stdout.write(self.style.SUCCESS('Successfully cleared existing data'))

          # Create Users
          user1 = User.objects.create_user(username='john_doe', email='john@example.com', password='password123')
          user2 = User.objects.create_user(username='jane_smith', email='jane@example.com', password='password123')

          # Create Pictures
          picture1 = Picture.objects.create(user=user1, image='shared_pics/fireworks.jpg', title='Fireworks',
                                            description='Stunning firework display', era='2010-2020')
          picture2 = Picture.objects.create(user=user2, image='shared_pics/glasgow_cityscape_copy.jpg',
                                            title='Quintessential Glasgow', description='As title', era='2000-2010')

          # Create Comments
          Comment.objects.create(user=user1, image=picture1, comment_body='Amazing!')
          Comment.objects.create(user=user2, image=picture1, comment_body='Superb!')
          Comment.objects.create(user=user2, image=picture2, comment_body='I love this place!')

          # Create ImageTags
          ImageTag.objects.create(picture=picture1, tag_label='fireworks')
          ImageTag.objects.create(picture=picture1, tag_label='night')
          ImageTag.objects.create(picture=picture2, tag_label='Glasgow')
          ImageTag.objects.create(picture=picture2, tag_label='cityscape')

          # Create Likes
          PictureLike.objects.create(user=user1, image=picture2)
          PictureLike.objects.create(user=user2, image=picture1)

          self.stdout.write(self.style.SUCCESS('Successfully inserted initial data'))
