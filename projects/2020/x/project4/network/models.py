from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    follow = models.ManyToManyField('User', through='Followers', related_name="followers", symmetrical=False)
    # def get_followers(self):
    #     return Followers.objects.filter(followee = self.user)

    # def get_following(self):
    #     return Followers.objects.filter(following = self.user)

class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    body = models.CharField(blank=False, max_length=280)
    timestamp = models.DateTimeField(auto_now_add=True)
    # likes = models.PositiveIntegerField(default=0)

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "body": self.body,
            "timestamp": self.timestamp.strftime("%b %#d %Y, %#I:%M %p"),
        }


class Followers(models.Model):
    followee = models.ForeignKey(User, related_name="followee", on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.followee} is following {self.following}'
