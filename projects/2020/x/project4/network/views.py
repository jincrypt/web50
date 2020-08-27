import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.core import serializers

from .models import User, Post, Followers


def index(request):
    return render(request, "network/index.html")


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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def profile(request, owner):
    user = User.objects.get(username=owner)
    posts = user.posts.all().order_by('-timestamp')
    # ! this might be able to be done via fetch?
    # ! maybe the fetch will only update followers?
    # Followers (who is following owner)
    followers = Followers.objects.filter(following=user.id)
    # Following (who is owner following?)
    following = Followers.objects.filter(followee=user.id)

    return render(request, "network/profile.html", {
        "owner": owner,
        "followers": followers,
        "following": following,
        "posts": posts
    })


def UserRelationship(request, owner):

    followee_user = User.objects.get(username=request.user)
    following_user = User.objects.get(username=owner)
    
    try: 
        relationship = Followers.objects.get(followee=followee_user.id, following=following_user.id)
    except:
        relationship = False

    if request.method == "GET":
        if relationship:
            return JsonResponse({"message": 'User is currently following'}, status=204)
        else:
            return JsonResponse({"message": 'User is not a follower'}, status=200)
        

    if request.method == "PUT":
        if relationship:
            relationship.delete()
            return JsonResponse({"message": f'{followee_user} is no longer following {following_user}.'}, status=204)
        else:
            new_following = Followers(followee=followee_user, following=following_user)
            try:
                new_following.full_clean()
                new_following.save()
                return JsonResponse({"message": f'{followee_user} is now following {following_user}.'}, status=204)
            except ValidationError as e:
                return JsonResponse({"message": e.message_dict['body']}, status=400)


def FollowerCount(request, owner):
    owner = User.objects.get(username=owner).id
    follower_count = Followers.objects.filter(following=owner).count()
    return JsonResponse({'follower_count': follower_count}) 


def posts(request):
    if request.method == "POST":
        data = json.loads(request.body)
        owner = request.user
        body = data.get("body")
        new_post = Post(
            user = owner,
            body = body
        )
        try:
            new_post.full_clean()
            new_post.save()
            return JsonResponse({"message": "New Post Created Successfully."}, status=201)
        except ValidationError as e:
            return JsonResponse({"message": e.message_dict['body']}, status=400)

    else:
        posts = Post.objects.all()
        posts = posts.order_by("-timestamp").all()
        return JsonResponse([post.serialize() for post in posts], safe=False)

def edit_post(request, post_id):
    if request.method == "PUT":
        post_edit = Post.objects.get(id=post_id)
        data = json.loads(request.body)

        post_edit.body = data['new_body']

        try:
            post_edit.full_clean()
            post_edit.save()
            return JsonResponse({"message": "Post Updated Successfully."}, status=204)
        except ValidationError as e:
            return JsonResponse({"message": e.message_dict['body']}, status=400)

def reload_post(request, post_id):
    if request.method == "GET":
        post = Post.objects.get(id=post_id)
        if request.user == post.user:
            return JsonResponse(post.serialize())
        else:
            return JsonResponse({"message": "Bad Actor"}, status=400)