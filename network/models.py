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

    def serialize(self):
        return {
            "id": self.id,
            "owner": self.owner.username,
            "description": self.description,
            "dateandhour": self.dateandhour.strftime("%b %d %Y, %I:%M %p"),
            "likedby": [user.username for user in self.likedby.all()]
        }

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)