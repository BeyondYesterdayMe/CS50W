from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime


from .models import User, Item, AuctionListing, Bid

# 으악 졸려... 오 ㅐ안돼...
def get_highest_bidder(auction_id):
    user_id = 0
    bid_price = 0
    auction = AuctionListing.objects.get(pk=auction_id)
    if auction:
        highest_bid = auction.bids.last()
        if highest_bid:
            user_id = highest_bid.user.id
            bid_price = highest_bid.price
    return user_id, bid_price

def index(request): 
    listings = AuctionListing.objects.all()
    highest_bid_infos = {}
    for it in listings:
        userid, price = get_highest_bidder(it.id)
        highest_bid_infos[it.id] = (userid, price)

    return render(request, "auctions/index.html", {
        "listings" : listings,
        "highest_bid_infos" : highest_bid_infos
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def createlisting(request):
    if request.method == "POST":
        try:    
            # add new item
            item = Item(name=request.POST.get("name"), desc=request.POST.get("desc"), img=request.POST.get("imageUrl"))
            item.save()

            # add new listing
            listing = AuctionListing(item=item, owner=request.user, start_price=int(request.POST.get("startprice")))
            listing.save()
        except Exception as e:
            return render(request, "auctions/createlisting.html", {
                "message" : str(e)
            })

        return HttpResponseRedirect(reverse("index"))

    return render(request, "auctions/createlisting.html")

def listing(request, auction_id):
    auction = AuctionListing.objects.get(pk=auction_id)
    if auction is None:
        return HttpResponseRedirect(reverse("index"))  

    bid_count = auction.bids.count()
    highest_bid = auction.bids.last() 
    cur_highest_user_id = 0 if highest_bid is None else highest_bid.user.id
    cur_highest_bid = 0 if highest_bid is None else highest_bid.price 

    in_watchlist = False
    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.id)
        if user:
            in_watchlist = any(watch.id == auction_id for watch in user.watchlist.all())

    user_id = 0 if user is None else user.id
    am_I_highest_bidder = False if cur_highest_user_id != user_id else True

    if request.method == "POST":
        if user is None:
            return HttpResponseRedirect(reverse("index")) 

        action = request.POST.get("action")
        if action is None:
            return HttpResponseRedirect(reverse("index")) 

        # watchlist add or remove
        if action == "watch_toggle":
            if in_watchlist:
                user.watchlist.remove(auction)    
            else:
                user.watchlist.add(auction)
            in_watchlist = not in_watchlist
            user.save()

            return render(request, "auctions/listing.html", {
                "message" : "Change Watchlist",
                "auction" : auction,
                "in_watchlist" : in_watchlist,
                "bid_count" : bid_count,
                "cur_highest_bid" : cur_highest_bid,
                "am_I_highest_bidder" : am_I_highest_bidder
            })
        
        # bidding
        if action == "bid":
            if request.POST.get("bidprice"):
                user_bid = int(request.POST.get("bidprice"))
                if cur_highest_bid < user_bid:
                    bid = Bid(user = user, price = user_bid)
                    bid.save()
                    auction.bids.add(bid)
                    auction.save()
                    bid_count += 1
                    return render(request, "auctions/listing.html", {
                        "message" : "Bidding OK",
                        "auction" : auction,
                        "in_watchlist" : in_watchlist,
                        "bid_count" : bid_count,
                        "cur_highest_bid" : user_bid,
                        "am_I_highest_bidder" : True
                    })
                else:
                    return render(request, "auctions/listing.html", {
                        "message" : "You need to bid more than...",
                        "auction" : auction,
                        "in_watchlist" : in_watchlist,
                        "bid_count" : bid_count,
                        "cur_highest_bid" : cur_highest_bid,
                        "am_I_highest_bidder" : False
                    })    
            else:
                return render(request, "auctions/listing.html", {
                    "message" : "You need to bid more than...",
                    "auction" : auction,
                    "in_watchlist" : in_watchlist,
                    "bid_count" : bid_count,
                    "cur_highest_bid" : cur_highest_bid,
                    "am_I_highest_bidder" : False
                })
        
    return render(request, "auctions/listing.html", {
            "message" : "Nothing changed",
            "auction" : auction,
            "in_watchlist" : in_watchlist,
            "bid_count" : bid_count,
            "cur_highest_bid" : cur_highest_bid,
            "am_I_highest_bidder" : am_I_highest_bidder
        })
    
def category(request):
    return render(request, "auctions/category.html")

def watchlist(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))
    
    user = User.objects.get(pk=request.user.id)
    if user is None:
        return HttpResponseRedirect(reverse("index"))
    
    return render(request, "auctions/watchlist.html", {
        "watchlist" : user.watchlist.all()
    })

def bidding(request, auction_id):
    # todo.
    return HttpResponseRedirect(reverse("index"))