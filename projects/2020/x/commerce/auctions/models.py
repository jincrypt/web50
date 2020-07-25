from django.contrib.a`u`th.models import AbstractUser
from django.db import models


class User(AbstractUser):
    comment = 
    pass

class Listings(models.Model):
    pass
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    bid
    image = models.ImageField()

class Bids():
    pass

class Comments():
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name=)

    pass
