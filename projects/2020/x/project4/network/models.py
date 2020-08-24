from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

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

# class Email(models.Model):
#     user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="emails")
#     sender = models.ForeignKey("User", on_delete=models.PROTECT, related_name="emails_sent")
#     recipients = models.ManyToManyField("User", related_name="emails_received")
#     subject = models.CharField(max_length=255)
#     body = models.TextField(blank=True)
#     timestamp = models.DateTimeField(auto_now_add=True)
#     read = models.BooleanField(default=False)
#     archived = models.BooleanField(default=False)

#     def serialize(self):
#         return {
#             "id": self.id,
#             "sender": self.sender.email,
#             "recipients": [user.email for user in self.recipients.all()],
#             "subject": self.subject,
#             "body": self.body,
#             "timestamp": self.timestamp.strftime("%b %#d %Y, %#I:%M %p"),
#             "read": self.read,
#             "archived": self.archived
#         }