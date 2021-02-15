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
    posts = Post.objects.all().order_by('-dateandhour')
    paginator = Paginator(posts, 10)
    
    if request.method == "POST":
        obj = Post()

        obj.owner = User.objects.get(id = request.user.id)
        obj.description = request.POST["description"]
        obj.dateandhour = datetime.datetime.now()
        obj.save()
        if request.GET.get("page") != None:
            try:
                posts = paginator.page(request.GET.get("page"))
            except:
                posts = paginator.page(1)
        else:
            posts = paginator.page(1)
        return render(request, 'network/index.html', {'posts': posts})
    else:
        if request.GET.get("page") != None:
            try:
                posts = paginator.page(request.GET.get("page"))
            except:
                posts = paginator.page(1)
        else:
            posts = paginator.page(1)
        return render(request, 'network/index.html', {'posts': posts})

@login_required
@csrf_exempt
def follow(request):
    if request.method == "POST":
        user = request.POST.get('user')
        action = request.POST.get('action')

        if action == 'Follow':
            try:
                # add user to current user's following list
                user = User.objects.get(username=user)
                profile = Follower.objects.get(user=request.user)
                profile.following.add(user)
                profile.save()

                # add current user to  user's follower list
                profile = Follower.objects.get(user=user)
                profile.follower.add(request.user)
                profile.save()
                return JsonResponse({'status': 201, 'action': "Unfollow", "follower_count": profile.follower.count()}, status=201)
            except:
                return JsonResponse({}, status=404)
        else:
            try:
                # add user to current user's following list
                user = User.objects.get(username=user)
                profile = Follower.objects.get(user=request.user)
                profile.following.remove(user)
                profile.save()

                # add current user to  user's follower list
                profile = Follower.objects.get(user=user)
                profile.follower.remove(request.user)
                profile.save()
                return JsonResponse({'status': 201, 'action': "Follow", "follower_count": profile.follower.count()}, status=201)
            except:
                return JsonResponse({}, status=404)

    return JsonResponse({}, status=400)
        
@login_required
def following(request):
    following = Follower.objects.get(user=request.user).following.all()
    posts = Post.objects.filter(owner__in=following).order_by('-dateandhour')
    paginator = Paginator(posts, 10)
    if request.GET.get("page") != None:
        try:
            posts = paginator.page(request.GET.get("page"))
        except:
            posts = paginator.page(1)
    else:
        posts = paginator.page(1)
    return render(request, 'network/following.html', {'posts': posts})

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
        profile = Follower()
        profile.user = user
        profile.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def profile(request, username):
    if request.method == "GET":
        profileuser = User.objects.get(username = username)
        actualuser = User.objects.get(id = request.user.id)
        posts = Post.objects.filter(owner = profileuser.id).order_by('-dateandhour')
        followed = Follower.objects.filter(following = profileuser.id, follower = actualuser.id)
        follower = Follower.objects.filter(following = profileuser)
        followings = Follower.objects.filter(follower = profileuser)
        users_profile = Follower.objects.get(user = actualuser )
        paginator = Paginator(posts, 10)
        totalfollower = len(follower)
        totalfollowing = len(followings)
        profile = Follower.objects.get(user = profileuser)
        for i in users_profile.follower.all():
            print(i)
        if profileuser.id != actualuser.id:
            if request.GET.get("page") != None:
                try:
                    posts = paginator.page(request.GET.get("page"))
                except:
                    posts = paginator.page(1)
            else:
                posts = paginator.page(1)
        
            return render(request, "network/profile.html", {
                "profileuser": profileuser,
                "posts": posts,
                "followed": followed,
                "followers": totalfollower,
                "followings": totalfollowing,
                "users_profile": users_profile,
                "profile": profile
            })
        else:
            if request.GET.get("page") != None:
                try:
                    posts = paginator.page(request.GET.get("page"))
                except:
                    posts = paginator.page(1)
            else:
                posts = paginator.page(1)
        
            return render(request, "network/profile.html", {
                "profileuser": profileuser,
                "posts": posts,
                "profileowner": 'Welcome to your profile.',
                "followed": followed,
                "followers": totalfollower,
                "followings": totalfollowing,
                "users_profile": users_profile,
                "profile": profile
            })