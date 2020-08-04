from django.contrib.auth.models import AbstractUser
from django.db import models

# classes should be camelcase
# variables should be underscored lowercase

class User(AbstractUser):
    watchlist = models.ManyToManyField('Listing', blank=True, related_name="watchlist")

class Listing(models.Model):
    title           = models.CharField(max_length=100)
    description     = models.CharField(max_length=500)
    date            = models.DateTimeField(auto_now_add=True)
    starting_price  = models.DecimalField(max_digits=11, decimal_places=2)                      # highest sold item in the world was 450million, so 11 digits should suffice
    owner           = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    image           = models.URLField(blank=True) # Default max_length=200
    status          = models.BooleanField(default=True)
    category        = models.ForeignKey('Categories', null=True, related_name="listing_category", on_delete=models.SET_NULL)

    

class Bid(models.Model):
    user    = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid_user")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bid_listing")
    bid     = models.DecimalField(max_digits=11, decimal_places=2)


class Comment(models.Model):
    user    = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_user")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comment_listing")
    comment = models.TextField(max_length=600)
    date    = models.DateTimeField(auto_now_add=True)


class Categories(models.Model):
    category = models.CharField(max_length=10)

# class Watchlist(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist_user")
#     listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watchlist_listing")