from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid
from .forms import CreateListingForm, CreateBid
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
                Bid(bid=bid, user=request.user, listing=Listing.objects.get(id=listing.id)).save()
    else:
        bid_form = CreateBid()


    return render(request, "auctions/listing.html", {
        "listing": listing,
        "bids": listing.bid_listing.all().order_by('-bid'),
        "bid_form": bid_form,
        "alert": alert
    })


def create_listing(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))


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

def close_listing(request, listing_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    if Listing.objects.get(pk=listing_id).owner == request.user:
        listing = Listing.objects.get(pk=listing_id)
        listing.status = False
        listing.save()

    return HttpResponseRedirect(reverse("listing", kwargs={"listing_id": listing_id}))