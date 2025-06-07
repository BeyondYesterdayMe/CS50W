from django.contrib.auth.models import AbstractUser
from django.db import models

#class ItemCategory(models.Model):
#    category = models.CharField(max_length=64)

class Item(models.Model):
    name = models.CharField(max_length=64)
    desc = models.CharField(max_length=64)
    #category = models.ForeignKey("ItemCategory", on_delete=models.CASCADE)
    img = models.URLField()

    #def __str__(self):
    #    return f"{self.name} and{self.desc}"

class AuctionListing(models.Model):
    item = models.ForeignKey("Item", on_delete=models.CASCADE)
    owner = models.ForeignKey("User", on_delete=models.CASCADE)
    start_price = models.PositiveIntegerField()
    #current_price = models.PositiveIntegerField()
    #hightest_bid = models.ForeignKey("Bid", on_delete=models.CASCADE, related_name="highest_for_listing", null=True, blank=True)
    created_date = models.DateTimeField(auto_now=True)
    bids = models.ManyToManyField("Bid", related_name="bids_for_listing")
    comments = models.ManyToManyField("Comment")

class Bid(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    price = models.PositiveIntegerField()

class Comment(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    comment = models.CharField(max_length=64)

class User(AbstractUser):
    watchlist = models.ManyToManyField("AuctionListing", related_name="watcher", null=True, blank=True)

    def __str__(self):
        return self.get_full_name()

