from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Follower(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followwho")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followedby")

class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="postowner")
    description = models.CharField(max_length=255)
    dateandhour = models.DateTimeField()
    likedby = models.ManyToManyField(User, blank=True, default=None, related_name="user_likes")

    @property
    def num_likes(self):
        return self.likedby.all().count()


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)