from django.contrib import admin

from .models import Item, AuctionListing, Bid, Comment, User
# Register your models here.
class ItemAdmin(admin.ModelAdmin):
    list_display = ("name", "desc", "img")

class AuctionListingAdmin(admin.ModelAdmin):
    list_display = ("item_name", "owner", "start_price", "created_date")

    def item_name(self, obj):
        return obj.item.name

class UserAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name")
    

admin.site.register(Item, ItemAdmin)
admin.site.register(AuctionListing, AuctionListingAdmin)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(User, UserAdmin)