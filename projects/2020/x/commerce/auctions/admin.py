from django.contrib import admin
from .models import User, Listing, Bid, Categories

# Register your models here.
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(User)
admin.site.register(Categories)
