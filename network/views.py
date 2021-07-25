from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
import json

from .models import User, Post, Like


def index(request):
    if request.method == "POST":
        text = request.POST['text']
        author = request.user
        post = Post.objects.create(text=text, author=author)
        post.save()
    posts = Post.objects.all()
    return render(request, "network/index.html", {'posts':posts})


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

def like_unlike(request):
    # pour la method get prévoir la récupération des query string user et post et retourner l'object json
    if request.method == "POST":
        # print(json.load(request)['user'])
        likeRequest = json.load(request)
        # check if like exist
        try:
            likeConstraint = Like.objects.get(user__username=likeRequest['user'], post__id=likeRequest['post'])
            print('Le like existe déjà')
            return JsonResponse({'foo':'bar'})
        except:
            post = Post.objects.get(id=likeRequest['post'])
            user = User.objects.get(username=likeRequest['user'])
            like = Like.objects.create(user=user, post=post)
            like.save()
            return JsonResponse({'foo':'bar'})