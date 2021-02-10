from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

import datetime


from .models import *


def index(request):
    if request.method == "POST":
        obj = Post()

        obj.owner = User.objects.get(id = request.user.id)
        obj.description = request.POST["description"]
        obj.dateandhour = datetime.datetime.now()
        obj.save()
        return render(request, "network/index.html", {
            "posts": Post.objects.all().order_by()
        })
    else:
        return render(request, "network/index.html", {
            "posts": Post.objects.all()
        })

@login_required
@csrf_exempt
def likeposts(request):
    if request.method == "POST":
        post_id = request.POST.get('id')
        is_liked = request.POST.get('is_liked')
        try:
            post = Post.objects.get(id=post_id)
            if is_liked == 'no':
                post.likedby.add(request.user)
                is_liked = 'yes'
            elif is_liked == 'yes':
                post.likedby.remove(request.user)
                is_liked = 'no'
            post.save()

            return JsonResponse({'like_count': post.likedby.count(), 'is_liked': is_liked, "status": 201})
        except:
            return JsonResponse({'error': "Post not found", "status": 404})
    return JsonResponse({}, status=400)

def listposts(request):
    posts = Post.objects.all()

    posts = posts.order_by("-dateandhour").all()
    return JsonResponse([post.serialize() for post in posts], safe=False)


def listprofileposts(request, username):
    posts = Post.objects.filter(owner = User.objects.get(username = username))

    posts = posts.order_by("-dateandhour").all()
    return JsonResponse([post.serialize() for post in posts], safe=False)

@login_required
@csrf_exempt
def edit_post(request):
    if request.method == "POST":
        post_id = request.POST.get('id')
        new_post = request.POST.get('post')
        try:
            post = Post.objects.get(id=post_id)
            if post.owner == request.user:
                post.description = new_post.strip()
                post.save()
                return JsonResponse({}, status=201)
        except:
            return JsonResponse({}, status=404)

    return JsonResponse({}, status=400)

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


def profile(request, username):
    if request.method == "GET":
        profileuser = User.objects.get(username = username)
        actualuser = User.objects.get(id = request.user.id)
        profilepost = Post.objects.filter(owner = profileuser.id)
        followed = Follower.objects.filter(following = profileuser.id, follower = actualuser.id)
        follower = Follower.objects.filter(following = profileuser)
        followings = Follower.objects.filter(follower = profileuser)
        totalfollower = len(follower)
        totalfollowing = len(followings)
        if profileuser.id != actualuser.id:
            return render(request, "network/profile.html", {
                "profileuser": profileuser,
                "profilepost": profilepost,
                "followed": followed,
                "followers": totalfollower,
                "followings": totalfollowing
            })
        else:
            return render(request, "network/profile.html", {
                "profileuser": profileuser,
                "profilepost": profilepost,
                "profileowner": "you are the owner",
                "followers": totalfollower,
                "followings": totalfollowing
            })
    else:
        profileuser = User.objects.get(username = username)
        actualuser = User.objects.get(id = request.user.id)
        profilepost = Post.objects.filter(owner = profileuser.id)
        obj = Follower.objects.filter(following = profileuser.id, follower = actualuser.id)
        if obj:
            obj.delete()
            followed = Follower.objects.filter(following = profileuser.id, follower = actualuser.id)
            follower = Follower.objects.filter(following = profileuser)
            followings = Follower.objects.filter(follower = profileuser)
            totalfollower = len(follower)
            totalfollowing = len(followings)
            return HttpResponseRedirect(reverse("profile", args=(username,)))
        else:
            obj = Follower()
            obj.following = profileuser
            obj.follower = actualuser
            obj.save()
            followed = Follower.objects.filter(following = profileuser.id, follower = actualuser.id)
            follower = Follower.objects.filter(following = profileuser)
            followings = Follower.objects.filter(follower = profileuser)
            totalfollower = len(follower)
            totalfollowing = len(followings)
            return HttpResponseRedirect(reverse("profile", args=(username,)))