from django.contrib.auth.models import AbstractUser
from django.db import models

# classes should be camelcase
# variables should be underscored lowercase

class User(AbstractUser):
    # bids = models.ManyToManyField(Bids, blank=True, related_name="bids")

    pass
    

class Listing(models.Model):
    title           = models.CharField(max_length=100)
    description     = models.CharField(max_length=500)
    date            = models.DateTimeField(auto_now_add=True)
    starting_price  = models.DecimalField(max_digits=11, decimal_places=2)                      # highest sold item in the world was 450million, so 11 digits should suffice
    owner           = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    image           = models.URLField(blank=True) # Default max_length=200
    status          = models.BooleanField(default=True)
    # highest_bid     = models.ForeignKey(Bid.aggregate(Max('bid')), related_name="highest_bid" )
    # owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    # price = models.ForeignKey(Bids, on_delete=models.CASCADE, related_name="bids")
    # comment = models.ForeignKey(Comments, on_delete=models.CASCADE, related_name="Comments")

class Bid(models.Model):
    user    = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid_user")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bid_listing")
    bid     = models.DecimalField(max_digits=11, decimal_places=2)
    # starting_bid = models.DecimalField(decimal_places=2)
    # current_bid = models.DecimalField(decimal_places=2)


class Comment():
    # comment = models.CharField(max_length=200)

    # listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name=)

    pass
