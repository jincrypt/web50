from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Bid, Comment
from .forms import CreateListingForm, CreateBid, CreateComment
from django.db.models import Max


def index(request):
    active_listings = Listing.objects.filter(status="True")
    return render(request, "auctions/index.html", {
        "active_listings": active_listings
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


def listing(request,listing_id):
    try:
        listing = Listing.objects.get(id=listing_id)
        comment_form = CreateComment()
        alert = None
    except Listing.DoesNotExist:
        raise Http404("Listing not found.")

    if request.method == "POST":
        bid_form = CreateBid(request.POST)

        if bid_form.is_valid():
            bid = bid_form.cleaned_data['bid']
            if listing.bid_listing.all():
                highest_bid = listing.bid_listing.all().last().bid
            else:
                highest_bid = 0.00
            
            if bid <= highest_bid or bid < listing.starting_price:
                # Bid can be same as starting price
                alert = "Bid is too low."
            else:
                Bid(bid=bid, user=request.user, listing=Listing.objects.get(id=listing_id)).save()
    else:
        bid_form = CreateBid()

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "bids": listing.bid_listing.all().order_by('-bid'),
        "bid_form": bid_form,
        "alert": alert,
        "comment_form": comment_form,
        "comments": listing.comment_listing.all()
    })


@login_required
def create_listing(request):
    if request.method == "POST":
        form = CreateListingForm(request.POST)
        
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            starting_price = form.cleaned_data['starting_price']
            owner = request.user
            image = form.cleaned_data['image']
            
            Listing(title=title, description=description, starting_price=starting_price, owner=owner, image=image).save()
            return HttpResponseRedirect(reverse("index"))
    else:
        form = CreateListingForm()

    return render(request, 'auctions/create.html', {
        'form': form
    })
    

@login_required
def close_listing(request, listing_id):
    if Listing.objects.get(pk=listing_id).owner == request.user:
        listing = Listing.objects.get(pk=listing_id)
        listing.status = False
        listing.save()

    return HttpResponseRedirect(reverse("listing", kwargs={"listing_id": listing_id}))


@login_required
def comment_listing(request, listing_id):
    if request.method == "POST":
        comment_form = CreateComment(request.POST)

        if comment_form.is_valid():
            comment_text = comment_form.cleaned_data['comment']
            Comment(listing=Listing.objects.get(id=listing_id), user=request.user, comment=comment_text).save()

    return HttpResponseRedirect(reverse("listing", kwargs={"listing_id": listing_id}))


@login_required
def watchlist_listing(request, listing_id, action):
    if request.method == "POST":
        listing = Listing.objects.get(id=listing_id)
        if action == "add":
            request.user.watchlist.add(listing)
        else:
            request.user.watchlist.remove(listing)

    return HttpResponseRedirect(reverse("listing", kwargs={"listing_id": listing_id}))

@login_required
def watchlist(request):
    return render(request, 'auctions/watchlist.html')